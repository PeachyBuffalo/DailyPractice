import { promises as fs } from 'fs';
import { Task } from './types';

export class TaskManager {
  private tasks: Task[] = [];
  private readonly filePath = 'tasks.json';

  constructor() {
    this.loadTasks();
  }

  private async loadTasks(): Promise<void> {
    try {
      const data = await fs.readFile(this.filePath, 'utf8');
      this.tasks = JSON.parse(data);
    } catch (error) {
      this.tasks = [];
    }
  }

  private async saveTasks(): Promise<void> {
    await fs.writeFile(this.filePath, JSON.stringify(this.tasks, null, 2));
  }

  async addTask(title: string): Promise<Task> {
    const task: Task = {
      id: Date.now(),
      title,
      completed: false,
      createdAt: new Date()
    };
    this.tasks.push(task);
    await this.saveTasks();
    return task;
  }

  async listTasks(): Promise<Task[]> {
    return this.tasks;
  }

  async completeTask(id: number): Promise<boolean> {
    const task = this.tasks.find(t => t.id === id);
    if (task) {
      task.completed = true;
      await this.saveTasks();
      return true;
    }
    return false;
  }

  async deleteTask(id: number): Promise<boolean> {
    const initialLength = this.tasks.length;
    this.tasks = this.tasks.filter(t => t.id !== id);
    if (this.tasks.length !== initialLength) {
      await this.saveTasks();
      return true;
    }
    return false;
  }
} 