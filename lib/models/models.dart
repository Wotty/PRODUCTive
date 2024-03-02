// Task model

class Task {
  final String id;
  final String projectId; // ID of the project this task belongs to

  final String name;

  final String description;

  final DateTime expectedCompletionDate;

  final int progress; // Progress percentage

  final bool completed;

  Task({
    required this.id,
    required this.projectId,
    required this.name,
    required this.description,
    required this.expectedCompletionDate,
    required this.progress,
    required this.completed,
  });
}

// Subtask model

class Subtask {
  final String id;

  final String taskId; // ID of the task this subtask belongs to

  final String name;

  final String description;

  final String color;

  final int progress; // Progress percentage

  final bool completed;

  Subtask({
    required this.id,
    required this.taskId,
    required this.name,
    required this.description,
    required this.color,
    required this.progress,
    required this.completed,
  });
}

// Workout model

class Workout {
  final String id;

  final String userId; // ID of the user who recorded this workout

  final String name;

  final String description;

  final String category;

  final List<Exercise> exercises;

  final List<String> bodyGroups;

  final List<WorkoutRecord> records;

  final List<WorkoutPlan> plans;

  Workout({
    required this.id,
    required this.userId,
    required this.name,
    required this.description,
    required this.category,
    required this.exercises,
    required this.bodyGroups,
    required this.records,
    required this.plans,
  });
}

// User model

class User {
  final String id;
  final String name;
  final String email;
  final String gender;

  User({
    required this.id,
    required this.name,
    required this.email,
    required this.gender,
  });
}
// Project model

class Project {
  final String id;

  final String userId; // ID of the user who owns this project

  final String name;

  final String description;

  final String category;

  final String color;

  final DateTime expectedCompletionDate;

  final int progress; // Progress percentage

  final bool completed;

  Project({
    required this.id,
    required this.userId,
    required this.name,
    required this.description,
    required this.category,
    required this.color,
    required this.expectedCompletionDate,
    required this.progress,
    required this.completed,
  });
}

// Exercise model

class Exercise {
  final String name;

  final String description;

  final String bodyGroup;

  Exercise({
    required this.name,
    required this.description,
    required this.bodyGroup,
  });
}

// WorkoutRecord model

class WorkoutRecord {
  final DateTime time;

  final String exerciseName;

  final List<ExerciseSet> sets;

  WorkoutRecord({
    required this.time,
    required this.exerciseName,
    required this.sets,
  });
}

// ExerciseSet model

class ExerciseSet {
  final DateTime timeCompleted;

  final double weight;

  final int reps;

  final double theoreticalMax;

  ExerciseSet({
    required this.timeCompleted,
    required this.weight,
    required this.reps,
    required this.theoreticalMax,
  });
}

// WorkoutPlan model

class WorkoutPlan {
  final String name;

  final String description;

  final String bodyGroup;

  final int numberOfSets;

  final List<Exercise> exercises;

  WorkoutPlan({
    required this.name,
    required this.description,
    required this.bodyGroup,
    required this.numberOfSets,
    required this.exercises,
  });
}

// UserMetrics model

class UserMetrics {
  final String id;

  final String userId; // ID of the user who recorded these metrics

  final DateTime dateTime;

  final double weight;

  final double bodyFat;

  final double height;

  final int age;

  final double
      competency; // Calculated column based on weight, age, and SBD numbers

  UserMetrics({
    required this.id,
    required this.userId,
    required this.dateTime,
    required this.weight,
    required this.bodyFat,
    required this.height,
    required this.age,
    required this.competency,
  });
}

// Note model

class Note {
  final String id;

  final String userId; // ID of the user who created this note

  final String name;

  final String contents;

  Note({
    required this.id,
    required this.userId,
    required this.name,
    required this.contents,
  });
}
