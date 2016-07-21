/**
 * Javascript for the scheduler page
 * Created by jbuoni on 4/21/16.
 * @namespace Scheduler
 */

/**
 * Create click handlers
 * @memberOf Scheduler
 */
function docready() {

    $('#runSchedulerBtn').on('click', _getCourseData);
    
    $('.capacity').on('change', function() {
        $('tr.item').each(function() {
            $this = $(this);
            capacity = $this.find('.capacity').val();
            $this.find('.ta-pool').val(Math.ceil(capacity / 50));
        });

    });

}

/**
 * Build courses array from table data
 * @private
 * @memberOf Scheduler
 */
function _getCourseData() {
    var courses = [];

    $('tr.item').each(function() {
        $this = $(this);

        var capacity = $this.find('.capacity').val();
        var offered = $this.find('.checkbox').is('checked') ? 1 : 2;
        var courseId = $this.find('.course-id').html();

        var fallTerm, springTerm, summerTerm, availability;

        fallTerm = 0;
        springTerm = 0;
        summerTerm = 0;
        
        if(offered) {
            switch (semester) {
                case 1:
                    fallTerm = 1;
                    availability = 'Fall Only';
                    break;
                case 2:
                    springTerm = 1;
                    availability = 'Spring Only';
                    break;
                case 3:
                    summerTerm = 1;
                    availability = 'Summer Only';
                    break;
            }
        }

        var course = {
            capacity: capacity,
            availability: availability,
            id: courseId,
            fallTerm: fallTerm,
            springTerm: springTerm,
            summerTerm: summerTerm
            
        };

        courses.push(course);
    });

    _saveCourseData(courses, _runGurobi);
}

/**
 * @typeDef {Object} Course
 * @property {Number} capacity
 * @property {String} availabity
 * @property {Number} id
 * @property {Number} fallTerm
 * @property {Number} springTerm
 * @property {Number} summerTerm
 */

/**
 * Save course data to database
 * @param {Array<Course>} courses
 * @param {function} callback
 * @memberOf Scheduler
 * @private
 */
function _saveCourseData(courses, callback) {
    $.ajax({
        type: "POST",
        url: 'http://127.0.0.1:5000/api/admin/update_courses',
        data: JSON.stringify({courses: courses}),
        contentType: 'application/json;charset=UTF-8',
        success: callback
    });
}

/**
 * Run gurobi scheduler
 * @private
 * @memberOf Scheduler
 */
function _runGurobi() {
    $.ajax({
        type: "POST",
        url: 'http://127.0.0.1:5000/api/admin/run_scheduler',
        contentType: 'application/json;charset=UTF-8',
        success: function() {
            alert('Scheduler started!');
        }
    });
}
