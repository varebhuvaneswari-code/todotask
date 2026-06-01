function addTask(){

    let taskInput =
    document.getElementById("taskInput");

    let deadlineInput =
    document.getElementById("deadlineInput");

    let task =
    taskInput.value.trim();

    let deadline =
    deadlineInput.value;

    if(task === ""){
        showAlert("Enter Task Name", "danger");
        return;
    }

    let li =
    document.createElement("li");

    li.className =
    "list-group-item";

    li.innerHTML = `

        <div class="d-flex justify-content-between align-items-center flex-wrap">

            <div>

                <div class="task-title">
                    ${task}
                </div>

                <div class="deadline">
                    Deadline:
                    ${formatDate(deadline)}
                </div>

            </div>

            <div class="mt-2">

                <button class="btn btn-success btn-sm"
                onclick="completeTask(this)">

                    Complete

                </button>

                <button class="btn btn-danger btn-sm"
                onclick="deleteTask(this)">

                    Delete

                </button>

            </div>

        </div>
    `;

    document
    .getElementById("taskList")
    .appendChild(li);

    checkDeadline(li, deadline);

    showAlert("Task Added Successfully", "success");

    taskInput.value = "";
    deadlineInput.value = "";
}

function deleteTask(button){

    button.parentElement
    .parentElement
    .parentElement
    .remove();

    showAlert("Task Deleted", "warning");
}

function completeTask(button){

    let taskItem =
    button.parentElement
    .parentElement
    .parentElement;

    taskItem.classList.toggle("completed");

    showAlert("Task Completed", "success");
}

function showAlert(message, type){

    let alertBox =
    document.getElementById("alertBox");

    alertBox.innerHTML = `

        <div class="alert alert-${type}">
            ${message}
        </div>

    `;

    setTimeout(() => {
        alertBox.innerHTML = "";
    }, 3000);
}

function formatDate(dateTime){

    if(dateTime === ""){
        return "No Deadline";
    }

    let date =
    new Date(dateTime);

    return date.toLocaleString();
}

function searchTask(){

    let input =
    document.getElementById("searchInput")
    .value
    .toLowerCase();

    let tasks =
    document.querySelectorAll("#taskList li");

    tasks.forEach(task => {

        let text =
        task.innerText.toLowerCase();

        if(text.includes(input)){
            task.style.display = "";
        }
        else{
            task.style.display = "none";
        }

    });
}

function checkDeadline(taskElement, deadline){

    if(deadline === ""){
        return;
    }

    let deadlineTime =
    new Date(deadline).getTime();

    let currentTime =
    new Date().getTime();

    let difference =
    deadlineTime - currentTime;

    if(difference <= 3600000 && difference > 0){

        taskElement.style.border =
        "2px solid orange";

        showAlert(
            "Task Deadline Approaching",
            "warning"
        );
    }

    if(difference < 0){

        taskElement.style.border =
        "2px solid red";

        showAlert(
            "Task Deadline Missed",
            "danger"
        );
    }
}