let localInstancesCache = [];

function loadTitleInstances() {
    const titleId = document.getElementById('task-title-select').value;
    const empRow = document.getElementById('employee-row');
    const empDropdown = document.getElementById('task-employee-select');
    
    document.getElementById('display-task-id').value = '';
    document.getElementById('task-completed-select').value = '0';

    if (!titleId) {
        empRow.style.display = 'none';
        return;
    }

    fetch(`/api/title/${titleId}/instances`)
        .then(res => res.json())
        .then(instances => {
            localInstancesCache = instances;
            
            if (instances.length === 0) {
                empRow.style.display = 'none';
                return;
            }

            empDropdown.innerHTML = '<option value="">-- Choose Employee --</option>';
            instances.forEach(ins => {
                empDropdown.innerHTML += `<option value="${ins.task_id}">${ins.employee_name}</option>`;
            });

            empRow.style.display = 'flex';
        });
}

function loadSpecificInstance() {
    const taskId = document.getElementById('task-employee-select').value;
    
    if(!taskId) {
        document.getElementById('display-task-id').value = '';
        document.getElementById('task-completed-select').value = '0';
        return;
    }

    const selectedInstance = localInstancesCache.find(item => item.task_id == taskId);
    if(selectedInstance) {
        document.getElementById('display-task-id').value = selectedInstance.task_id;
        document.getElementById('task-completed-select').value = selectedInstance.completed;
    }
}

function submitStatusUpdate() {
    const taskId = document.getElementById('display-task-id').value;
    const completedVal = document.getElementById('task-completed-select').value;

    if(!taskId) {
        alert("Please pick an active employee first.");
        return;
    }

    fetch('/api/tasks/update_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            task_id: taskId,
            completed: parseInt(completedVal)
        })
    })
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            alert("Database synchronized successfully!");
            const titleId = document.getElementById('task-title-select').value;
            fetch(`/api/title/${titleId}/instances`)
                .then(res => res.json())
                .then(updated => { localInstancesCache = updated; });
        }
    });
}

function createNewTask(event) {
    event.preventDefault();
    const titleId = document.getElementById('ins-title').value;
    const employeeId = document.getElementById('ins-employee').value;
    const completed = document.getElementById('ins-completed').value;

    fetch('/api/tasks/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title_id: titleId,
            employee_id: employeeId,
            completed: completed
        })
    })
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            alert(data.message);
            window.location.href = '/dashboard';
        }
    });
}