import asyncio
from datetime import timedelta
from typing import (
    Any,
    Callable,
    Optional,
    ParamSpec,
    TypeVar,
    Union,
    overload,
)

from loguru import logger

from agentifyme.config import BaseModule, WorkflowConfig
from agentifyme.errors import AgentifyMeExecutionError, AgentifyMeValidationError, ErrorContext
from agentifyme.utilities.func_utils import (
    execute_function,
    get_function_metadata,
)

P = ParamSpec("P")
R = TypeVar("R", bound=Callable[..., Any])


class Workflow(BaseModule):
    def __init__(self, config: WorkflowConfig, *args, **kwargs) -> None:
        super().__init__(config, **kwargs)
        self.config = config
        self.run_id = None

    def run(self, *args, **kwargs: Any) -> Any:
        logger.info(f"Running workflow: {self.config.name}")
        if self.config.func:
            kwargs.update(zip(self.config.func.__code__.co_varnames, args))
            try:
                return execute_function(self.config.func, kwargs)
            except Exception as e:
                raise AgentifyMeExecutionError(
                    message=f"Error executing workflow {self.config.name}: {str(e)}",
                    context=ErrorContext(component_type="workflow", component_id=self.config.name),
                    execution_state=kwargs,
                ) from e
        else:
            raise AgentifyMeValidationError(
                message="Workflow function not implemented",
                context=ErrorContext(component_type="workflow", component_id=self.config.name),
            )

    async def arun(self, *args, **kwargs: Any) -> Any:
        logger.info(f"Running async workflow: {self.config.name}")
        if self.config.func:
            kwargs.update(zip(self.config.func.__code__.co_varnames, args))
            try:
                if asyncio.iscoroutinefunction(self.config.func):
                    return await self.config.func(**kwargs)
                else:
                    return await asyncio.to_thread(self.config.func, **kwargs)
            except Exception as e:
                raise AgentifyMeExecutionError(
                    message=f"Error executing workflow {self.config.name}: {str(e)}",
                    context=ErrorContext(component_type="workflow", component_id=self.config.name),
                    execution_state=kwargs,
                ) from e
        else:
            raise AgentifyMeValidationError(
                message="Workflow function not implemented",
                context=ErrorContext(component_type="workflow", component_id=self.config.name),
            )


@overload
def workflow(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator function for defining a workflow."""


@overload
def workflow(*, name: str, description: Optional[str] = None) -> Callable[..., Any]: ...


# Implement the function
def workflow(
    func: Union[Callable[..., Any], None] = None,
    *,
    name: Optional[str] = None,
    description: Optional[str] = None,
    schedule: Optional[Union[str, timedelta]] = None,
) -> Callable[..., Any]:
    def decorator(func: Callable[..., Any], outer_name: Optional[str] = name) -> Callable[..., Any]:
        func_metadata = get_function_metadata(func)
        _name = func_metadata.name
        if outer_name:
            _name = outer_name
        _workflow = WorkflowConfig(
            name=_name,
            description=description or func_metadata.description,
            slug=_name.lower().replace(" ", "_"),
            func=func,
            input_parameters=func_metadata.input_parameters,
            output_parameters=func_metadata.output_parameters,
            schedule=schedule,
        )
        _workflow_instance = Workflow(_workflow)
        WorkflowConfig.register(_workflow_instance)

        def wrapper(*args, **kwargs) -> Any:
            kwargs.update(zip(func.__code__.co_varnames, args))
            result = _workflow_instance(**kwargs)
            return result

        async def async_wrapper(*args, **kwargs) -> Any:
            kwargs.update(zip(func.__code__.co_varnames, args))
            result = await _workflow_instance.arun(**kwargs)
            return result

        # Choose the appropriate wrapper based on whether the function is async or not
        final_wrapper = async_wrapper if asyncio.iscoroutinefunction(func) else wrapper

        final_wrapper.__agentifyme = _workflow_instance  # type: ignore
        final_wrapper.__agentifyme_metadata = {  # type: ignore
            "type": "workflow",
            "name": _workflow.name,
            "description": _workflow.description,
            "input_parameters": {name: param.name for name, param in _workflow.input_parameters.items()},
            "output_parameters": [param.name for param in _workflow.output_parameters],
            "nested_calls": [],
            "is_async": asyncio.iscoroutinefunction(func),
        }

        return final_wrapper

    if callable(func):
        return decorator(func)
    elif name is not None:
        return decorator
    else:
        raise AgentifyMeValidationError(
            message="Invalid arguments for workflow decorator",
            context=ErrorContext(component_type="workflow", component_id="decorator"),
        )
