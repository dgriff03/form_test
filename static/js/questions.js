const TIME_PER_QUESTION = 3 * 60 * 1000;

let eval_id;
let question_list;

let current_question = 0;

const answers = [];

let interval_id = 0;

function complete() {
    if (interval_id) {
        clearInterval(interval_id);
        interval_id = 0;
    }
    let data = {};
    data['eval_id'] = eval_id;
    data['answers'] = answers;
    $.ajax({
      type: "POST",
      url: '/evaluation',
      data: JSON.stringify(data),
      contentType: 'application/json',
    });
    // TODO(Daniel): Show an error on failure.
    $('#exam-form').hide();
    $('#complete').show();

}

function next() {
    answers.push($('#question_answer').val());
    $('#question_answer').val('');
    let last_question = question_list.length -1;
    if (current_question >= last_question) {
        complete();
    }
    current_question += 1;
    if (current_question == last_question) {
        $('#next-button').text('Submit');
    }
    $('#current-question-count').text(current_question + 1);
    $('#question-title').text(question_list[current_question]);
    start_timer();
}

function zero_pad(s) {
    return s.length == 1 ? '0' + s : s;
}

function format_time_string(milliseconds) {
    let seconds = milliseconds / 1000;
    seconds.toFixed(0);
    let minutes = Math.floor(seconds / 60) + '';
    seconds = Math.floor(seconds % 60) + '';
    return zero_pad(minutes) + ':' + zero_pad(seconds);
}


function start_timer() {
    if (interval_id) {
        clearInterval(interval_id);
        interval_id = 0;
    }
    let end_time = TIME_PER_QUESTION + Date.now();

    interval_id = setInterval(() => {
        const time_remaining = end_time - Date.now();
        if (time_remaining <= 0) {
            next();
            interval_id = 0;
            clearInterval(interval_id);
            return;
        }
        $('#time-remaining').text(format_time_string(time_remaining));
    }, 100);

}
