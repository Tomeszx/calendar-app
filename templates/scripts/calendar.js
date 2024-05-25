function get_new_month(direction) {
    let date_string = document.getElementById('monthYear').getAttribute('title').toString();
    let date_parts = date_string.split('.');
    let current_date = new Date(date_parts[2], Number(date_parts[1]) - 1, 1);
    let new_date = new Date(current_date.setMonth(current_date.getMonth() + direction))
    let date_year_path = new_date.getFullYear().toString() + '/' + String(new_date.getMonth() + 1)
    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/date/" + date_year_path,
        success: function (month) {
            replace_new_month(month, new_date);
        },
    });
}

function replace_new_month(month, date) {
    let newContent = document.createElement('div');
    newContent.id = 'weeks'
    month.weeks.forEach((week) => {
        let weekDiv = document.createElement('div');
        weekDiv.className = 'week';

        week.days.forEach((day) => {
            let button = document.createElement('button');
            if (date.day !== 0){
                button.name = day.date;
            }
            button.className = day.status;
            button.textContent = day.month_index;
            button.setAttribute("onclick", "open_iframe(event)")
            weekDiv.appendChild(button);
        });
        newContent.appendChild(weekDiv);
    });

    let date_header = document.getElementById('monthYear')
    date_header.textContent = date.toLocaleString('default', {month: 'long', year: 'numeric'}).toUpperCase()
    date_header.title = date.toLocaleString('default', {year: 'numeric', month: 'numeric', day: 'numeric'})
    let element = document.getElementById('weeks');
    element.replaceWith(newContent);
}

function open_iframe(event) {
    let date = event.target.getAttribute('name');
    let iframeContent = document.getElementById('iframeContent');
    iframeContent.src = '/templates/form.html';
    document.getElementById('iframePopup').style.display = 'block';

    iframeContent.onload = function() {
        let iframeDoc = iframeContent.contentDocument || iframeContent.contentWindow.document;
        let dateInput = iframeDoc.getElementsByName('date')[0];
        if (dateInput) {
            dateInput.value = date;
        }
    };
}

// When the user clicks on <span> (x), close the modal
document.getElementById('closeIframe').onclick = function () {
    document.getElementById('iframePopup').style.display = 'none';
    document.getElementById('iframeContent').src = '';
    get_new_month(0);
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    var iframePopup = document.getElementById('iframePopup');
    if (event.target === iframePopup) {
        iframePopup.style.display = 'none';
        document.getElementById('iframeContent').src = '';
        get_new_month(0);
    }
}
