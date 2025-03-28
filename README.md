# CPU_Scheduling_simulator
An implementation of various CPU scheduling algorithms in python. The algorithms included are First Come First Serve (FCFS), Round Robin (RR), Shortest Process First (SJF) and prioriy scheduling.

# Algorithms:
# First Come First Serve (FCFS)

First Come First Serve (FCFS) is a scheduling algorithm in which the process that arrives first is executed first. It is a simple and easy-to-understand algorithm, but it can lead to poor performance if there are processes with long burst times. This algorithm does not have any mechanism for prioritizing processes, so it is considered a non-preemptive algorithm.

In FCFS scheduling, the process that arrives first is executed first, regardless of its burst time or priority. This can lead to poor performance, as longer running processes will block shorter ones from being executed. It is commonly used in batch systems where the order of the processes is important.

# Shortest Job First (SJF)

Shortest Job First (SJF) is a scheduling algorithm where the process with the smallest burst time is executed first. This algorithm can be preemptive (Shortest Remaining Time First, SRTF) or non-preemptive, depending on whether a newly arrived process with a shorter burst time can interrupt an ongoing process.

SJF scheduling improves efficiency by reducing the average waiting time and turnaround time, as shorter processes are completed quickly. However, it suffers from starvation, where longer processes may never get executed if shorter processes keep arriving. This algorithm is commonly used in situations where process execution times are known in advance, such as in batch systems.

# Priority Scheduling

Priority Scheduling is a scheduling algorithm in which each process is assigned a priority, and the process with the highest priority is executed first. This algorithm can be preemptive or non-preemptive, depending on whether a higher-priority process can interrupt a running process.

Processes can be assigned priorities based on factors such as urgency, importance, or resource requirements. However, a major issue with Priority Scheduling is starvation, where low-priority processes may never get executed if high-priority processes keep arriving. A common solution to this problem is aging, where the priority of a process increases over time to ensure it eventually gets executed.

# Round Robin (RR) with Varying Time Quantum
Round Robin (RR) with variable quantum is a scheduling algorithm that uses a time-sharing approach to divide CPU time among processes. In this version of RR, the quantum (time slice) is not fixed and can be adjusted depending on the requirements of the processes. This allows processes with shorter burst times to be given smaller quanta and vice versa.

The algorithm works by maintaining a queue of processes, where each process is given a quantum of time to execute on the CPU. When a process's quantum expires, it is moved to the back of the queue, and the next process in the queue is given a quantum of time to execute.

The variable quantum allows the algorithm to be more efficient as it allows the CPU to spend more time on shorter processes and less time on longer ones. This can help to minimize the average waiting time for processes. Additionally, it also helps to avoid the issue of starvation, which occurs when a process with a long burst time prevents other processes from executing.

# Steps to Run the Python File
Install Python
Ensure that Python is installed on your system. You can check by running:

python --version
If Python is not installed, download and install it from Python's official website.

Install Required Libraries
The simulator may use the following Python libraries:
matplotlib (for Gantt chart visualization)
numpy (for mathematical operations)
pandas (for data handling)

Install them using pip:
pip install matplotlib numpy pandas
Run the Python File

# Navigate to the folder where the Python script is stored and run:

python filename.py
Replace filename.py with the actual name of your Python file.

