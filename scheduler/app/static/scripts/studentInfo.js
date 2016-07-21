/**
 * @namespace StudentInfo
 */

var $coursesModal, $questionsModal, $specialization;

function docready() {
    $specialization = $('#specialization');
    //Replace unicode characters
    $specialization.html($specialization.html().replace('(', '').replace(')', '').replace(',', '').replace('\'', '').replace('\'', ''));

    _generateClickHandlers();
    _generatePreferenceTable();

    $('#courseBtn').on('click', _addCourse);
    $('#questionBtn').on('click', _addQuestion);
}

/**
 * Create click handlers
 * @private
 * @memberof StudentInfo
 */
function _generateClickHandlers() {

    $('.glyphicon-arrow-up').on('click', function(event) {
        var courseRow = event.target.parentElement.parentElement.parentElement;
        var courseID = courseRow.id;
        var $courseRow = $('#' + courseID);

        $courseRow.prev().before($courseRow);

        _updateStudentPreferences(_getCourseIds(), function(err, result) {
            if(err)
                console.log(err);
            else
                console.log(result);
        });

        _generatePreferenceTable();
    });

    $('.glyphicon-arrow-down').on('click', function(event) {
        var courseID = event.target.parentElement.parentElement.parentElement.id;
        var $courseRow = $('#' + courseID);
        $courseRow.next().after($courseRow);

        _updateStudentPreferences(_getCourseIds(), function(err, result) {
            if(err)
                console.log(err);
            else
                console.log(result);
        });

        _generatePreferenceTable();
    });

    $('.glyphicon-remove').on('click', function(event) {
        var courseID = event.target.parentElement.parentElement.parentElement.id;
        var $courseRow = $('#' + courseID);
        $courseRow.remove();

        _updateStudentPreferences(_getCourseIds(), function(err, result) {
            if(err)
                console.log(err);
            else
                console.log(result);
        });

        _generatePreferenceTable();
    });

    $('#addPreference').on('click', function() {
        $coursesModal = $('#coursesModal').modal();
        $coursesModal.modal('show');
    });

    $('#addQuestion').on('click', function() {
        $questionsModal = $('#questionsModal').modal();
        $questionsModal.modal('show');
    });
}

/**
 * Add course to the course preferences table
 * @private
 * @memberof StudentInfo
 */
function _addCourse() {

    var courseRowId = $('#courseAddSelect').val().replace('course', '');
    var alreadyAdded = false;

    $('.preference-table-row').each(function () {
        if(this.id === courseRowId)
            alreadyAdded = true;
    });

    if(alreadyAdded) {
        $('.add-course-error').text('Course already added to preferences');
    } else {

        var courseIDs = _getCourseIds();
        courseIDs.push(courseRowId);

        var _updateTable = function(err, response) {
            $('#preferencesTable > tbody:last-child').append('<tr id="' + courseRowId + '" class="preference-table-row">' +
                '<td>' + $('#courseAddSelect :selected').text() + '<span class="pull-right">' +
                '<span class="glyphicon glyphicon-arrow-up icon_padding"></span>' +
                '<span class="glyphicon glyphicon-arrow-down icon_padding"></span>' +
                '<span class="glyphicon glyphicon-remove icon_padding"></span>' +
                '</span></td></tr>'
            );

            _generateClickHandlers();
        };

        _updateStudentPreferences(courseIDs, _updateTable);
        _generatePreferenceTable();
        $coursesModal.modal('hide');
    }
}

/**
 * Returns course id in preference order
 * @returns {Object[]}
 * @private
 * @memberof StudentInfo
 */
function _getCourseIds() {
    var courseIDs = [];

    $('.preference-table-row').each(function () {
        courseIDs.push(this.id);
    });

    return courseIDs;
}

/**
 * AJAX call to update student preferences
 * @param {Object[]} courseIDs
 * @param {function} callback
 * @private
 * @memberof StudentInfo
 */
function _updateStudentPreferences(courseIDs, callback) {

    var requestData = {
        semester: semester,
        courseIDs: courseIDs
    };

    $.ajax({
        type: "POST",
        url: 'http://127.0.0.1:5000/api/students/' + username + '/preferences',
        data: JSON.stringify({preferences: requestData}),
        contentType: 'application/json;charset=UTF-8',
        success: callback
    });
}

/**
 * Call API to save question to database
 * @param question
 * @param callback
 * @private
 * @memberOf StudentInfo
 */
function _updateQuestions(question, callback) {
    $.ajax({
            type: "POST",
            url: 'http://127.0.0.1:5000/api/students/' + username + '/question',
            data: JSON.stringify({question: question}),
            contentType: 'application/json;charset=UTF-8',
            success: callback
    });
}

/**
 * Add question to the questions table
 * @private
 * @memberof StudentInfo
 */
function _addQuestion() {
    var question = $('textarea#questionTextArea').val();

    $('#questionsTable > tbody:last-child').append('<tr><td>' +
         question + '</td><td></td></tr>' /**<span class="glyphicon glyphicon-ok pull-right"></span></td></tr>'**/
    );

    _updateQuestions(question, function(err, result) {
        if(err)
            console.log(err);
        else
            console.log(result);
    });
}

/**
 * Updates the table and hides / shows arrow information depending on the position of each row item and the number of rows
 * @private
 * @memberof StudentInfo
 */
function _generatePreferenceTable() {

    var $firstSpanDownArrow = $('#preferencesTable tbody tr:first-child span.glyphicon-arrow-down');
    var $secondChildSpan = $('#preferencesTable tbody tr:nth-child(2) span.glyphicon-arrow-up');
    var $preferencesTableBody = $('#preferencesTable tbody tr');

    if($secondChildSpan)
        $secondChildSpan.show();


    if($preferencesTableBody.length == 1)
        $firstSpanDownArrow.hide();
     else
        $firstSpanDownArrow.show();


    $('#preferencesTable tbody tr:first-child span.glyphicon-arrow-up').hide();

}

/**
 * Unbind events
 * @param {function} callback
 * @private
 * @memberof StudentInfo
 */
function _unbindEvents(callback) {
    $('.glyphicon-arrow-up').off("click");
    $('.glyphicon-arrow-down').off("click");
    $('.glyphicon-remove').off("click");
    $('#addPreference').off("click");
    $('#addQuestion').off("click");
    $('#courseBtn').off("click");
    $('#questionBtn').off("click");

    callback();
}