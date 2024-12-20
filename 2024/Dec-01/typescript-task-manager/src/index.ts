import * as readlineSync from 'readline-sync';
import { TaskManager } from './TaskManager';

// Add initial debug log
console.log('Starting Task Manager Application...');

class CLI {
  private taskManager: TaskManager;

  constructor() {
    this.taskManager = new TaskManager();
  }

  private showMenu(): void {
    console.log('\n=== Task Manager ===');
    console.log('1. Add Task');
    console.log('2. List Tasks');
    console.log('3. Complete Task');
    console.log('4. Delete Task');
    console.log('5. Exit');
  }

  async start(): Promise<void> {
    console.log('CLI Started');
    while (true) {
      this.showMenu();
      const choice = readlineSync.questionInt('Choose an option (1-5): ');

      switch (choice) {
        case 1:
          const title = readlineSync.question('Enter task title: ');
          await this.taskManager.addTask(title);
          console.log('Task added successfully!');
          break;

        case 2:
          const tasks = await this.taskManager.listTasks();
          console.log('\nTasks:');
          tasks.forEach(task => {
            console.log(`[${task.completed ? 'X' : ' '}] ${task.id}: ${task.title}`);
          });
          break;

        case 3:
          const completeId = readlineSync.questionInt('Enter task ID to complete: ');
          const completed = await this.taskManager.completeTask(completeId);
          console.log(completed ? 'Task completed!' : 'Task not found!');
          break;

        case 4:
          const deleteId = readlineSync.questionInt('Enter task ID to delete: ');
          const deleted = await this.taskManager.deleteTask(deleteId);
          console.log(deleted ? 'Task deleted!' : 'Task not found!');
          break;

        case 5:
          console.log('Goodbye!');
          return;

        default:
          console.log('Invalid option!');
      }
    }
  }
}

// Create and start the CLI
console.log('Initializing CLI...');
const cli = new CLI();
cli.start().catch(error => {
  console.error('Application error:', error);
  process.exit(1);
}); 