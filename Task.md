# Development Tasks

## Phase 1: Foundation

### Project Setup

- [ ] Initialize Django project
- [ ] Setup Git repository
- [ ] Create basic app structure (users, assignments, submissions)

### Authentication

- [ ] Student login system
- [ ] Lecturer login system
- [ ] Role-based access control

---

## Phase 2: Core Features

### Student Side

- [ ] Code editor page (basic textarea first)
- [ ] Input box for CLI input
- [ ] Run button
- [ ] Output display area
- [ ] Local auto-save (IndexedDB)

### Lecturer Side

- [ ] Create assignment page
- [ ] Define:
  - Title
  - Description
  - Sample input
  - Expected output
- [ ] View student submissions

---

## Phase 3: Execution Engine

### Docker Setup

- [ ] Install Docker
- [ ] Create Python execution container
- [ ] Write script to:
  - Accept code
  - Run inside container
  - Capture output

### Safety Controls

- [ ] Limit execution time (e.g. 2 seconds)
- [ ] Limit memory usage
- [ ] Kill infinite loops

### Integration

- [ ] Connect Django to execution script
- [ ] Return output to frontend

---

## Phase 4: Submission System

- [ ] Submit button
- [ ] Store student code
- [ ] Store output
- [ ] Compare with expected output
- [ ] Mark pass/fail

---

## Phase 5: Offline Support

- [ ] Implement IndexedDB storage
- [ ] Auto-save every few seconds
- [ ] Restore code on reload
- [ ] Handle reconnect sync (basic)

---

## Phase 6: Deployment

- [ ] Create Dockerfile for Django app
- [ ] Create docker-compose setup
- [ ] One-command startup script
- [ ] Test on local machine
- [ ] Test on low-spec server

---

## Phase 7: Testing

- [ ] Simulate 20–50 students
- [ ] Test slow internet conditions
- [ ] Test low-end Android devices
- [ ] Test failure cases:
  - server down
  - infinite loops
  - large outputs

---

## Phase 8: First Real Use

- [ ] Deploy to one campus server
- [ ] Run in a real class
- [ ] Collect feedback
- [ ] Identify breaking points

---

## Rules While Building

- Do not add features unless needed
- Do not support multiple languages yet
- Do not optimize prematurely
- Focus on reliability over performance

---

## Definition of Done (v1)

System is successful if:

- 30+ students can run Python code from phones
- Lecturer can create and review assignments
- System does not crash during a 1-hour lab