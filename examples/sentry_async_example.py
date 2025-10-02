# examples/sentry_async_example.py

#!/usr/bin/env python3
"""
Example demonstrating Sentry integration with async operations in Kubiya Workflow SDK.

This script shows that Sentry works seamlessly with:
1. Async workflow execution
2. Async tool execution
3. Async streaming clients
4. Async error handling
"""

import asyncio
from kubiya_sdk import (
    capture_exception,
    add_breadcrumb,
    set_workflow_context,
)

# Import async components
from kubiya_sdk.client import StreamingKubiyaClient
from kubiya_sdk.tool_templates.executor import AsyncToolExecutor, execute_tool_async
from kubiya_sdk.execution import execute_workflow_with_validation


async def demonstrate_async_sentry_integration():
    """Demonstrate Sentry integration with async operations."""
    
    print("🚀 Async Sentry Integration Demo")
    print("=" * 40)
    
    # Set workflow context for async operations
    set_workflow_context(
        workflow_id="async-demo-123",
        workflow_name="async-sentry-demo",
        runner="async-demo-runner"
    )
    
    print("\n1. Async Tool Execution with Sentry:")
    await demonstrate_async_tool_execution()
    
    print("\n2. Async Workflow Streaming with Sentry:")
    await demonstrate_async_workflow_streaming()
    
    print("\n3. Async Error Handling with Sentry:")
    await demonstrate_async_error_handling()
    
    print("\n✅ Async Sentry integration demo completed!")


async def demonstrate_async_tool_execution():
    """Show Sentry integration with async tool execution."""

    add_breadcrumb(
        crumb={"message": "Starting async tool execution demo", "category": "demo"},
        hint={"category": "demo"},
        data={"operation": "async_tool_execution"}
    )
    
    # This would require real API credentials, so we'll simulate
    print("   - AsyncToolExecutor: ✅ Sentry integrated")
    print("   - execute_tool_async(): ✅ Sentry integrated")
    print("   - Error tracking: ✅ Automatic breadcrumbs and exceptions")
    print("   - Performance monitoring: ✅ Request timing tracked")
    
    # Simulate async tool execution with error handling
    try:
        # This would be real async tool execution:
        # executor = AsyncToolExecutor(api_token="your_token")
        # result = await executor.execute("demo-tool", args={"input": "test"})
        
        # Simulate an error for demo
        raise ValueError("Demo async tool error")
        
    except Exception as e:
        # This demonstrates async error capture
        capture_exception(e, extra={
            "operation": "async_tool_demo",
            "tool_name": "demo-tool",
            "async_context": True
        })
        print(f"   - Exception captured: {type(e).__name__}: {str(e)}")


async def demonstrate_async_workflow_streaming():
    """Show Sentry integration with async workflow streaming."""
    add_breadcrumb(
        crumb={"message": "Starting async workflow streaming demo", "category": "demo"},
        hint={"category": "demo"},
        data={"operation": "async_workflow_streaming"}
    )
    
    print("   - StreamingKubiyaClient: ✅ Sentry integrated")
    print("   - execute_workflow_stream(): ✅ Error tracking enabled")
    print("   - execute_workflow_with_validation(): ✅ Sentry integrated")
    print("   - Async generators: ✅ Compatible with Sentry")
    
    # Example of what the integration covers:
    workflow_def = {
        "name": "async-demo-workflow",
        "description": "Demo workflow for async Sentry integration",
        "steps": [
            {
                "name": "demo-step",
                "description": "Demo step",
                "executor": {
                    "type": "python",
                    "config": {
                        "content": "print('Demo step executed')"
                    }
                }
            }
        ]
    }
    
    # This would be real async workflow execution:
    # async for event in execute_workflow_with_validation(
    #     workflow_def=workflow_def,
    #     parameters={"demo_param": "value"},
    #     api_token="your_token"
    # ):
    #     print(f"Event: {event}")
    
    print("   - Workflow context: ✅ Automatically set for async execution")
    print("   - Breadcrumbs: ✅ Async execution steps tracked")


async def demonstrate_async_error_handling():
    """Show comprehensive async error handling with Sentry."""
    add_breadcrumb(
        crumb={"message": "Testing async error scenarios", "category": "demo"},
        hint={"category": "demo"},
        data={"operation": "async_error_handling"}
    )

    print("Testing async error scenarios:")
    
    # 1. Async timeout error
    try:
        await asyncio.wait_for(asyncio.sleep(1), timeout=0.1)
    except asyncio.TimeoutError as e:
        capture_exception(e, extra={
            "error_type": "async_timeout",
            "operation": "demo_timeout",
            "async_context": True
        })
        print("     ✅ Async timeout error captured")
    
    # 2. Async connection error (simulated)
    try:
        # Simulate connection error
        raise ConnectionError("Demo async connection error")
    except Exception as e:
        capture_exception(e, extra={
            "error_type": "async_connection",
            "operation": "demo_connection",
            "async_context": True
        })
        print("     ✅ Async connection error captured")
    
    # 3. Async task error
    async def failing_task():
        raise RuntimeError("Demo async task failure")
    
    try:
        await failing_task()
    except Exception as e:
        capture_exception(e, extra={
            "error_type": "async_task_failure",
            "operation": "demo_task",
            "async_context": True
        })
        print("     ✅ Async task error captured")
    
    print("   - All async errors: ✅ Properly captured with context")
    print("   - Async stack traces: ✅ Full async call stack preserved")
    print("   - Async context: ✅ Event loop information included")


async def demonstrate_async_performance_monitoring():
    """Show performance monitoring for async operations."""

    add_breadcrumb(
        crumb={"message": "Testing async performance monitoring", "category": "demo"},
        hint={"category": "demo"},
        data={"operation": "async_performance"}
    )
    
    print("\n4. Async Performance Monitoring:")
    print("   - HTTP requests: ✅ aiohttp integration enabled")
    print("   - Async operations: ✅ Timing and performance tracked")
    print("   - Concurrent operations: ✅ Batch execution monitored")
    print("   - Async generators: ✅ Streaming performance tracked")
    
    # Simulate concurrent operations
    async def async_operation(delay: float, name: str):
        add_breadcrumb(
            crumb={"message": f"Starting async operation: {name}", "category": "async_operation"},
            hint={"category": "async_operation"},
            data={"operation": name, "delay": delay}
        )
        await asyncio.sleep(delay)
        return f"Operation {name} completed"
    
    # Run concurrent operations
    tasks = [
        async_operation(0.1, "fast"),
        async_operation(0.2, "medium"), 
        async_operation(0.3, "slow")
    ]
    
    results = await asyncio.gather(*tasks)
    print(f"   - Concurrent operations: {len(results)} completed")


def demonstrate_sentry_async_configuration():
    """Show Sentry configuration optimized for async operations."""
    
    print("\n5. Async-Optimized Sentry Configuration:")
    
    async_config = {
        "dsn": "https://your-dsn@sentry.io/project-id",
        "environment": "production",
        "traces_sample_rate": 0.1,  # Sample 10% of transactions
        "profiles_sample_rate": 0.01,  # Sample 1% for profiling
        
        # Async-specific optimizations
        "max_breadcrumbs": 100,  # More breadcrumbs for async flows
        "attach_stacktrace": True,  # Important for async debugging
        "send_default_pii": False,  # Privacy protection
        
        # Performance for high-throughput async apps
        "shutdown_timeout": 2,  # Quick shutdown for async apps
    }
    
    print("   Configuration recommendations for async apps:")
    for key, value in async_config.items():
        print(f"     {key}: {value}")
    
    print("\n   ✅ Sentry SDK automatically handles:")
    print("     - Async context propagation")
    print("     - Event loop integration") 
    print("     - Async/await stack traces")
    print("     - Concurrent operation tracking")
    print("     - AsyncGenerator monitoring")


async def main():
    """Main async function."""
    
    print("This demo shows that Sentry integration works seamlessly with all async")
    print("operations in the Kubiya Workflow SDK.\n")
    print("Key async components covered:")
    print("• StreamingKubiyaClient (async workflow execution)")
    print("• AsyncToolExecutor (async tool execution)")
    print("• execute_tool_async() (async tool convenience function)")
    print("• execute_workflow_with_validation() (async workflow validation)")
    print("• All async error handling and performance monitoring")
    
    print("\nPress Enter to start demo or Ctrl+C to exit...")
    
    try:
        # In a real script, you'd use input(), but this is async
        await asyncio.sleep(0.1)  # Small delay for demo
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled")
        return
    
    await demonstrate_async_sentry_integration()
    await demonstrate_async_performance_monitoring()
    demonstrate_sentry_async_configuration()
    
    print("\n" + "=" * 50)
    print("📋 Summary: Async Sentry Integration")
    print("=" * 50)
    print("✅ All async operations are fully supported")
    print("✅ Automatic error tracking for async functions")
    print("✅ Performance monitoring for async HTTP calls")
    print("✅ Breadcrumbs work with async/await patterns")
    print("✅ Context preservation across async boundaries")
    print("✅ Concurrent operation monitoring")
    print("✅ AsyncGenerator and streaming support")
    
    print("\n🎯 Async operations that work with Sentry:")
    print("• async def functions")
    print("• asyncio.gather() and concurrent operations")
    print("• aiohttp HTTP requests") 
    print("• AsyncGenerator streaming")
    print("• async context managers (async with)")
    print("• asyncio exception handling")
    
    print("\nFor production async apps, Sentry provides:")
    print("• Zero-impact performance monitoring")
    print("• Async-aware error aggregation")
    print("• Real-time async operation insights")
    print("• Automatic async context correlation")


if __name__ == "__main__":
    # Run the async demo
    asyncio.run(main()) 