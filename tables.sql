CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
	name varchar(255),
  	start_date DATE,
  	description varchar(1000)
);

CREATE TABLE sprints (
    id SERIAL PRIMARY KEY,
	name varchar(255),
  	start_date DATE,
  	end_date DATE,
  	description varchar(1000),
  	active boolean NOT NULL,
  	project_id INT,
  	CONSTRAINT project
      FOREIGN KEY(project_id)
	  REFERENCES projects(project_id)

);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
	name varchar(255),
  	start_date DATE,
  	description varchar(1000),
  	sprint_id INT,
  	CONSTRAINT sprint
      FOREIGN KEY(sprint_id)
	  REFERENCES sprints(sprint_id),
  	creator_id INT,
  	CONSTRAINT creator
      FOREIGN KEY(creator_id)
	  REFERENCES users(creator_id),
  	observers FOREIGN_KEY(users) [],
  	project_id INT,
  	CONSTRAINT project
      FOREIGN KEY(project_id)
	  REFERENCES projects(project_id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
	name varchar(255),
  	role
);

CREATE TABLE attachemnts (
    id SERIAL PRIMARY KEY,
	name varchar(255),
  	start_date DATE,
  	description varchar(1000),
  	file ,
  	task_id INT,
  	CONSTRAINT task
      FOREIGN KEY(task_id)
	  REFERENCES tasks(task_id),
  	uploader_id INT,
  	CONSTRAINT uploader
      FOREIGN KEY(uploader_id)
	  REFERENCES users(uploader_id),
);