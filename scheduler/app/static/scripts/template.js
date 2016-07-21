/**
 * TemplateHeader handles all menu related actions. Will also determine if user is or is not authenticated.
 * Created by jbuoni on 3/24/16.
 */
var templateHeader = (function() {

    var $errorText, $loginModal, _username;

    function _readCookie(name){
        name += '=';
        for (var ca = document.cookie.split(/;\s*/), i = ca.length - 1; i >= 0; i--)
            if (!ca[i].indexOf(name))
                return ca[i].replace(name, '');
    }

    /**
     * Call the Authentication API
     * @param callback {function}
     * @private
     */
    function _isAuthenticated() {
        _username = _readCookie('username');
        return _username;
    }

    /**
     * Initialize the template related tools. Determine if user is
     * authenticated or not.
     */
    function ready() {
        $loginModal = $('#loginModal').modal();
        $errorText = $('loginError');
        

        $errorText.hide();

        if(_isAuthenticated) {
            $loginModal.modal('hide');
        } else {
            $loginModal.modal('show');
        }
    }

    function login(username, password) {
        $.ajax({
            type: 'GET',
            url: 'http://127.0.0.1:5000/api/login/',
            data: {
                username: username,
                password: password
            },
            dataType: 'application/json',
            success: function(result) {
                if(result)
                    document.cookie = 'username=' + username;
                else
                    $errorText.show();
            },
            error: callback(err, null)

        });
    }

    function _highlightNavOption() {
        var url = window.location.href;

        if (url.indexOf('student_list') != - 1) {
            $('students').addClass('active');
        } else if(url.indexOf('user') != - 1) {
            $('student_info').addClass('active');
        } else if(url.indexOf('course_data') != - 1) {
            $('course_aggregate_data').addClass('active');
        } else if(url.indexOf('admin_info') != - 1) {
            $('admin_info').addClass('active');
        }
    }

    return {
        ready: ready,
        username: _username,
        login: login
    }
})();