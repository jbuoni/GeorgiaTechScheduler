/**
 * @namespace AdminInfo
 */

var $questionModal, $questionAnswerTextArea, currentQuestionId, answers;

/**
 * Generate click handlers for page
 * @memberOf AdminInfo
 */
function docready() {

    answers = {};

    $questionAnswerTextArea = $('textarea#questionTextArea');

    $('.unanswered_question_icon').hide();

    $('.unanswered-question-row').on('click', function(event) {
        //Question information is set in the row
        currentQuestionId = event.target.id.replace('answer', '');
        var questionText = event.target.innerHTML;
        var questionAnswer = _getQuestionAnswer();

        //Create modal
        $questionModal = $('#questionModal').modal();

        if(questionAnswer)
            $questionAnswerTextArea.val(questionAnswer);

        //Set modal text
        $('#questionModalQuestionText').html(questionText);
        $questionModal.modal('show');
    });
    
    $('.answered-question-row').on('click', function(event) {
        //Question information is set in the row
        currentQuestionId = event.target.id;
        var questionText = $('#' + currentQuestionId).html();
        var questionAnswer = _getQuestionAnswer();
        //Create modal
        $questionModal = $('#questionModal').modal();
        //Set modal text
        $('#questionModalQuestionText').html(questionText);

        $questionAnswerTextArea.val(questionAnswer);
        $questionModal.modal('show');
    });
    
    $('#questionBtn').on('click', _answerQuestion);
}

/**
 * Update mongo table with question answer.
 * @private
 * @memberOf AdminInfo
 */
function _answerQuestion() {

    var _callback = function (err, result) {
        if(result === 'success') {
            answers[currentQuestionId] = $questionAnswerTextArea.val();
            $('#' + currentQuestionId + 'icon').show();
            $('#' + currentQuestionId + 'answer > .answer_text').html($questionAnswerTextArea.val());
            console.log(result);
        }
    };

    var question = {
        id: currentQuestionId,
        answer: $questionAnswerTextArea.val()
    };

    $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:5000/api/admin/answer_question',
            data: JSON.stringify({question: question}),
            contentType: 'application/json;charset=UTF-8',
            success: _callback
    });
}

/**
 * Returns the question answer. Will be used to get the most up to date answer.
 * @returns {*}
 * @private
 * @memberOf AdminInfo
 */
function _getQuestionAnswer() {
    if(answers[currentQuestionId])
        return answers[currentQuestionId];

    var $currentTableRow = $('#' + currentQuestionId + 'answer > .answer_text');

    if($currentTableRow && $currentTableRow.html()) {
        return $currentTableRow.html().trim();
    }

    return undefined;
}