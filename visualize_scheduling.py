import matplotlib.pyplot as plt
import numpy as np
import json

def create_rm_gantt_chart(task_data, execution_time=0.1):
    """
    Create a Gantt chart for Rate-Monotonic scheduling visualization.
    
    Parameters:
    task_data (dict): Dictionary with task names as keys and firing times (single value or list) as values
    execution_time (float): Execution time for each task instance (in milliseconds)
    """
    
    # Set up the plot
    fig, ax = plt.subplots(figsize=(15, 5))
    
    # Colors for different tasks
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']
    
    # Track the y position for each task
    y_positions = {}
    for i, task in enumerate(reversed(task_data.keys())):
        y_positions[task] = i
    
    # Plot each task's execution periods
    for task_idx, (task_name, firing_time) in enumerate(task_data.items()):
        y_pos = y_positions[task_name]
        
        # Handle both single values and lists
        if isinstance(firing_time, (int, float)):
            firing_times = [firing_time]
        else:
            firing_times = firing_time
            
        # Create rectangles for each firing time
        for start_time in firing_times:
            ax.barh(y_pos, 
                   execution_time,
                   left=start_time,
                   height=0.3,
                   color=colors[task_idx % len(colors)],
                   alpha=0.8)
    
    # Customize the plot
    ax.set_yticks(list(range(len(task_data))))
    ax.set_yticklabels(list(reversed(task_data.keys())))
    
    ax.set_xlabel('Time (ms)')
    ax.set_title('Rate-Monotonic Scheduling Gantt Chart')
    
    # Add grid for better readability
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    # Set x-axis limits
    all_times = []
    for times in task_data.values():
        if isinstance(times, (int, float)):
            all_times.append(times)
        else:
            all_times.extend(times)
            
    min_time = min(all_times)
    max_time = max(all_times)
    ax.set_xlim(min_time - 0.5, max_time + execution_time + 0.5)
    
    plt.tight_layout()
    return fig, ax

if __name__ == "__main__":
	# Create and show the chart
	
	with open("result.json", 'r') as file:
		task_data: dict = json.load(file)
	
	del task_data["deadTime"]
	del task_data["sumDeadTime"]
	resolution = task_data["resolution"]
	del task_data["resolution"]

	fig, ax = create_rm_gantt_chart(task_data, resolution)
	plt.show()