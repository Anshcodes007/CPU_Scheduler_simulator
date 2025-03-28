import matplotlib.pyplot as plt
import matplotlib.patches as patches
from tkinter import *
from tkinter import ttk
import math

class Process:
    def __init__(self, pid, arrival, burst, priority=0):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.priority = priority
        self.finish_time = 0
        self.waiting_time = 0
        self.start_time = -1
        self.turnaround_time = 0

class CPUScheduler:
    def __init__(self, processes):
        self.processes = processes
        self.time = 0
        self.gantt_chart = []
    
    def reset_processes(self):
        for p in self.processes:
            p.remaining = p.burst
            p.finish_time = 0
            p.waiting_time = 0
            p.start_time = -1
            p.turnaround_time = 0
        self.time = 0
        self.gantt_chart = []
    
    def fcfs(self):
        """First Come First Serve (Non-preemptive)"""
        self.reset_processes()
        queue = sorted(self.processes, key=lambda x: x.arrival)
        
        for p in queue:
            p.waiting_time = max(0, self.time - p.arrival)
            p.start_time = max(self.time, p.arrival)
            self.time = p.start_time + p.burst
            p.finish_time = self.time
            p.turnaround_time = p.finish_time - p.arrival
            self.gantt_chart.append((p.pid, p.start_time, p.finish_time))
        
        return self.processes
    
    def sjf(self, preemptive=False):
        """Shortest Job First (Preemptive and Non-preemptive)"""
        self.reset_processes()
        completed = []
        ready_queue = []
        remaining = self.processes.copy()
        
        while remaining or ready_queue:
            # Add arriving processes to ready queue
            for p in remaining[:]:
                if p.arrival <= self.time:
                    ready_queue.append(p)
                    remaining.remove(p)
            
            if not ready_queue:
                self.time += 1
                continue
                
            if preemptive:
                ready_queue.sort(key=lambda x: x.remaining)
                current = ready_queue[0]
            else:
                ready_queue.sort(key=lambda x: x.burst)
                current = ready_queue[0]
            
            if current.start_time == -1:
                current.start_time = self.time
            
            if preemptive:
                # Run for 1 unit and check for new arrivals
                exec_start = self.time
                self.time += 1
                current.remaining -= 1
                self.gantt_chart.append((current.pid, exec_start, self.time))
                
                if current.remaining == 0:
                    current.finish_time = self.time
                    current.waiting_time = current.start_time - current.arrival
                    current.turnaround_time = current.finish_time - current.arrival
                    completed.append(current)
                    ready_queue.remove(current)
            else:
                # Run to completion
                exec_start = self.time
                self.time += current.remaining
                current.remaining = 0
                current.finish_time = self.time
                current.waiting_time = current.start_time - current.arrival
                current.turnaround_time = current.finish_time - current.arrival
                completed.append(current)
                ready_queue.remove(current)
                self.gantt_chart.append((current.pid, exec_start, self.time))
        
        return completed
    
    def round_robin(self, quantum=2):
        """Round Robin Scheduling"""
        self.reset_processes()
        queue = []
        completed = []
        remaining = self.processes.copy()
        
        while remaining or queue:
            # Add arriving processes to queue
            for p in remaining[:]:
                if p.arrival <= self.time:
                    queue.append(p)
                    remaining.remove(p)
            
            if not queue:
                self.time += 1
                continue
                
            current = queue.pop(0)
            
            if current.start_time == -1:
                current.start_time = self.time
            
            # Execute for quantum or remaining time
            exec_time = min(quantum, current.remaining)
            exec_start = self.time
            current.remaining -= exec_time
            self.time += exec_time
            self.gantt_chart.append((current.pid, exec_start, self.time))
            
            if current.remaining > 0:
                queue.append(current)
            else:
                current.finish_time = self.time
                current.waiting_time = current.start_time - current.arrival
                current.turnaround_time = current.finish_time - current.arrival
                completed.append(current)
        
        return completed
    
    def priority_scheduling(self, preemptive=False):
        """Priority Scheduling (Preemptive and Non-preemptive)"""
        self.reset_processes()
        completed = []
        ready_queue = []
        remaining = self.processes.copy()
        
        while remaining or ready_queue:
            # Add arriving processes to ready queue
            for p in remaining[:]:
                if p.arrival <= self.time:
                    ready_queue.append(p)
                    remaining.remove(p)
            
            if not ready_queue:
                self.time += 1
                continue
                
            # Sort by priority (lower number = higher priority)
            ready_queue.sort(key=lambda x: x.priority)
            current = ready_queue[0]
            
            if current.start_time == -1:
                current.start_time = self.time
            
            if preemptive:
                # Run for 1 unit and check for higher priority
                exec_start = self.time
                self.time += 1
                current.remaining -= 1
                self.gantt_chart.append((current.pid, exec_start, self.time))
                
                if current.remaining == 0:
                    current.finish_time = self.time
                    current.waiting_time = current.start_time - current.arrival
                    current.turnaround_time = current.finish_time - current.arrival
                    completed.append(current)
                    ready_queue.remove(current)
            else:
                # Run to completion
                exec_start = self.time
                self.time += current.remaining
                current.remaining = 0
                current.finish_time = self.time
                current.waiting_time = current.start_time - current.arrival
                current.turnaround_time = current.finish_time - current.arrival
                completed.append(current)
                ready_queue.remove(current)
                self.gantt_chart.append((current.pid, exec_start, self.time))
        
        return completed
    
    def calculate_metrics(self, scheduled_processes):
        """Calculate performance metrics"""
        total_wait = sum(p.waiting_time for p in scheduled_processes)
        total_turnaround = sum(p.turnaround_time for p in scheduled_processes)
        throughput = len(scheduled_processes) / max(p.finish_time for p in scheduled_processes) if scheduled_processes else 0
        
        return {
            "avg_wait": total_wait / len(scheduled_processes) if scheduled_processes else 0,
            "avg_turnaround": total_turnaround / len(scheduled_processes) if scheduled_processes else 0,
            "throughput": throughput,
            "total_time": max(p.finish_time for p in scheduled_processes) if scheduled_processes else 0
        }
    
    def plot_gantt_chart(self, title):
        """Plot Gantt chart using matplotlib"""
        if not self.gantt_chart:
            return
        
        fig, ax = plt.subplots(figsize=(10, 4))
        
        # Create a color map for processes
        colors = plt.cm.get_cmap('tab20', len(self.processes))
        process_ids = sorted(set(p.pid for p in self.processes))
        color_map = {pid: colors(i) for i, pid in enumerate(process_ids)}
        
        # Plot each process execution
        for i, (pid, start, end) in enumerate(self.gantt_chart):
            duration = end - start
            ax.barh(y=0, width=duration, left=start, 
                    color=color_map[pid], edgecolor='black')
            ax.text(start + duration/2, 0, f'P{pid}', 
                   ha='center', va='center', color='white')
        
        # Set chart properties
        ax.set_yticks([])
        ax.set_xlabel('Time')
        ax.set_title(f'Gantt Chart - {title}')
        ax.grid(axis='x')
        
        # Set x-axis ticks at integer values
        max_time = max(end for _, _, end in self.gantt_chart)
        ax.set_xticks(range(0, max_time + 2))
        
        plt.tight_layout()
        plt.show()

class SchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        
        # Process input frame
        self.input_frame = ttk.LabelFrame(root, text="Process Input")
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Process table
        self.tree = ttk.Treeview(self.input_frame, columns=("PID", "Arrival", "Burst", "Priority"), show="headings")
        self.tree.heading("PID", text="PID")
        self.tree.heading("Arrival", text="Arrival Time")
        self.tree.heading("Burst", text="Burst Time")
        self.tree.heading("Priority", text="Priority")
        self.tree.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
        
        # Input fields
        ttk.Label(self.input_frame, text="PID:").grid(row=1, column=0)
        self.pid_entry = ttk.Entry(self.input_frame)
        self.pid_entry.grid(row=1, column=1)
        
        ttk.Label(self.input_frame, text="Arrival:").grid(row=1, column=2)
        self.arrival_entry = ttk.Entry(self.input_frame)
        self.arrival_entry.grid(row=1, column=3)
        
        ttk.Label(self.input_frame, text="Burst:").grid(row=2, column=0)
        self.burst_entry = ttk.Entry(self.input_frame)
        self.burst_entry.grid(row=2, column=1)
        
        ttk.Label(self.input_frame, text="Priority:").grid(row=2, column=2)
        self.priority_entry = ttk.Entry(self.input_frame)
        self.priority_entry.grid(row=2, column=3)
        
        # Buttons
        self.add_btn = ttk.Button(self.input_frame, text="Add Process", command=self.add_process)
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=5)
        
        self.clear_btn = ttk.Button(self.input_frame, text="Clear All", command=self.clear_processes)
        self.clear_btn.grid(row=3, column=2, columnspan=2, pady=5)
        
        # Algorithm selection frame
        self.algo_frame = ttk.LabelFrame(root, text="Algorithm Selection")
        self.algo_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Algorithm options
        self.algo_var = StringVar(value="FCFS")
        algorithms = [
            ("FCFS (First Come First Serve)", "FCFS"),
            ("SJF (Non-preemptive)", "SJF_NP"),
            ("SJF (Preemptive)", "SJF_P"),
            ("Round Robin", "RR"),
            ("Priority (Non-preemptive)", "PRIORITY_NP"),
            ("Priority (Preemptive)", "PRIORITY_P")
        ]
        
        for i, (text, value) in enumerate(algorithms):
            ttk.Radiobutton(self.algo_frame, text=text, variable=self.algo_var, 
                           value=value).grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)
        
        # RR quantum input
        ttk.Label(self.algo_frame, text="RR Quantum:").grid(row=3, column=0, sticky="e")
        self.quantum_entry = ttk.Entry(self.algo_frame)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.grid(row=3, column=1, sticky="w")
        
        # Run button
        self.run_btn = ttk.Button(root, text="Run Simulation", command=self.run_simulation)
        self.run_btn.grid(row=2, column=0, pady=10)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(root, text="Results")
        self.results_frame.grid(row=0, column=1, rowspan=3, padx=10, pady=10, sticky="nsew")
        
        # Results text
        self.results_text = Text(self.results_frame, height=20, width=50)
        self.results_text.grid(row=0, column=0, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        
        # Sample data
        self.sample_processes = [
            Process(1, 0, 6, 3),
            Process(2, 2, 4, 2),
            Process(3, 4, 8, 1),
            Process(4, 6, 5, 4),
            Process(5, 8, 3, 0)
        ]
        self.load_sample_data()
    
    def add_process(self):
        try:
            pid = int(self.pid_entry.get())
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            priority = int(self.priority_entry.get()) if self.priority_entry.get() else 0
            
            self.tree.insert("", "end", values=(pid, arrival, burst, priority))
            
            # Clear entries
            self.pid_entry.delete(0, END)
            self.arrival_entry.delete(0, END)
            self.burst_entry.delete(0, END)
            self.priority_entry.delete(0, END)
        except ValueError:
            self.results_text.insert(END, "Error: Please enter valid numbers for all fields\n")
    
    def clear_processes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def load_sample_data(self):
        self.clear_processes()
        for p in self.sample_processes:
            self.tree.insert("", "end", values=(p.pid, p.arrival, p.burst, p.priority))
    
    def get_processes_from_table(self):
        processes = []
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            processes.append(Process(values[0], values[1], values[2], values[3]))
        return processes
    
    def run_simulation(self):
        processes = self.get_processes_from_table()
        if not processes:
            self.results_text.insert(END, "Error: No processes to schedule\n")
            return
        
        scheduler = CPUScheduler(processes)
        algorithm = self.algo_var.get()
        results = None
        title = ""
        
        self.results_text.delete(1.0, END)
        self.results_text.insert(END, "=== CPU Scheduling Simulation ===\n")
        self.results_text.insert(END, f"Number of processes: {len(processes)}\n")
        
        try:
            if algorithm == "FCFS":
                title = "First Come First Serve (FCFS)"
                results = scheduler.fcfs()
            elif algorithm == "SJF_NP":
                title = "Shortest Job First (Non-preemptive)"
                results = scheduler.sjf(preemptive=False)
            elif algorithm == "SJF_P":
                title = "Shortest Job First (Preemptive)"
                results = scheduler.sjf(preemptive=True)
            elif algorithm == "RR":
                quantum = int(self.quantum_entry.get())
                title = f"Round Robin (Quantum={quantum})"
                results = scheduler.round_robin(quantum=quantum)
            elif algorithm == "PRIORITY_NP":
                title = "Priority Scheduling (Non-preemptive)"
                results = scheduler.priority_scheduling(preemptive=False)
            elif algorithm == "PRIORITY_P":
                title = "Priority Scheduling (Preemptive)"
                results = scheduler.priority_scheduling(preemptive=True)
            
            # Display results
            self.results_text.insert(END, f"\nAlgorithm: {title}\n")
            self.results_text.insert(END, "PID | Arrival | Burst | Priority | Start | Finish | Waiting | Turnaround\n")
            self.results_text.insert(END, "-"*80 + "\n")
            
            for p in sorted(results, key=lambda x: x.pid):
                self.results_text.insert(END, 
                    f"{p.pid:3} | {p.arrival:7} | {p.burst:5} | {p.priority:8} | {p.start_time:5} | {p.finish_time:6} | {p.waiting_time:7} | {p.turnaround_time:9}\n")
            
            # Display metrics
            metrics = scheduler.calculate_metrics(results)
            self.results_text.insert(END, "\nPerformance Metrics:\n")
            self.results_text.insert(END, f"Average Waiting Time: {metrics['avg_wait']:.2f}\n")
            self.results_text.insert(END, f"Average Turnaround Time: {metrics['avg_turnaround']:.2f}\n")
            self.results_text.insert(END, f"Throughput: {metrics['throughput']:.2f} processes per unit time\n")
            self.results_text.insert(END, f"Total Simulation Time: {metrics['total_time']} units\n")
            
            # Show Gantt chart
            scheduler.plot_gantt_chart(title)
            
        except ValueError as e:
            self.results_text.insert(END, f"Error: {str(e)}\n")
        except Exception as e:
            self.results_text.insert(END, f"An error occurred: {str(e)}\n")

if __name__ == "__main__":
    root = Tk()
    app = SchedulerGUI(root)
    root.mainloop()