let eval_id;
let question_list;

let current_question = 0;

const answers = [];

function restart_timer() {

}

function complete() {
    console.log(answers);
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
    restart_timer();
}


function start_timer() {


}
