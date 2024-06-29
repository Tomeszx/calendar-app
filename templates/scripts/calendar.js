function get_new_month(direction) {
    document.getElementById('next').setAttribute('disabled', '')
    document.getElementById('prev').setAttribute('disabled', '')

    let element = document.getElementsByClassName('tab active')[0]
    let event = element.getAttribute('data-event')
    let date_string = document.getElementById('monthYear').getAttribute('title').toString();
    let date_parts = date_string.split('.');
    let current_date = new Date(date_parts[2], Number(date_parts[1]) - 1, 1);
    let new_date = new Date(current_date.setMonth(current_date.getMonth() + direction))
    let year = new_date.getFullYear().toString()
    let month = String(new_date.getMonth() + 1)
    $.ajax({
        type: "GET",
        url: `${document.URL}calendar?year=${year}&month=${month}&event=${event}`,
        success: function (month) {
            replace_new_month(month, new_date);
        },
    });
    document.getElementById('next').removeAttribute('disabled');
    document.getElementById('prev').removeAttribute('disabled');
}


function replace_new_month(month, date) {
    let newContent = document.createElement('div');
    newContent.id = 'weeks';
    month.days.forEach((day, index) => {
        if (index === 0 || index % 7 === 0) {
            let weekDiv = document.createElement('div');
            weekDiv.className = 'week';
            newContent.appendChild(weekDiv);
        }

        let button = document.createElement('button');
        if (date.day !== 0) {
            button.name = day.date;
        }

        button.className = day.status;
        if (day.max_events_num > 1) {
            let bottom_color = `#dadac7 ${day.percentage_filled}`;
            let top_color = `buttonface ${day.percentage_filled}`;
            button.style.background += `linear-gradient(to top, ${bottom_color}, ${top_color})`;
        }
        button.textContent = day.month_index;
        button.setAttribute("onclick", "open_iframe(event)");
        if (Date.parse(day.date) <= Date.now()){
            button.disabled = true
            button.style.pointerEvents = 'none'
        }
        newContent.lastChild.appendChild(button);
    });
    let calendar_navigation = document.getElementById('monthYear')
    calendar_navigation.textContent = date.toLocaleString('pl-PL', {month: 'long', year: 'numeric'}).toUpperCase()
    calendar_navigation.title = date.toLocaleString('pl-PL', {year: 'numeric', month: 'numeric', day: 'numeric'})
    document.getElementById('weeks').replaceWith(newContent);
}


function open_iframe(event) {
    let date = event.target.getAttribute('name');
    let event_type_elem = document.getElementsByClassName('tab active')[0]
    let event_type = event_type_elem.getAttribute('data-event')
    let iframeContent = document.getElementById('iframeContent');
    iframeContent.src = '/templates/form.html';
    document.getElementById('iframePopup').style.display = 'block';

    iframeContent.onload = function () {
        let iframeDoc = iframeContent.contentDocument || iframeContent.contentWindow.document;
        let dateInput = iframeDoc.getElementById('date');
        if (dateInput !== undefined){
            dateInput.value = date;
            iframeDoc.getElementById('event_type').value = event_type;
            iframeDoc.getElementById('first-step-title').textContent = event_type.replaceAll('_', ' ');
            iframeDoc.getElementById('first-step-subtitle').textContent = date;
        }
    }
}

$(document).ready(function () {
    $('.tab').on('click', function (e) {
        $('.tab').removeClass('active');
        $(this).addClass('active');
        get_new_month(0);

        let month = document.getElementById('month')
        if (month !== null){
            month.id += '-active'
            document.getElementById('guide').id += '-active'
        }
    });
});


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
