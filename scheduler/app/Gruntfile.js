/**
 * Gruntfile
 * this can be used to compile less files
 * feel free to add to the list below
 * for more information go to: http://gruntjs.com/
 *
 */
module.exports = function(grunt) {

    // Project configuration
    grunt.initConfig({

        // less task
        less: {
            development: {
                options: {
                    cleancss: false
                },
                files: grunt.file.readJSON('less_files.json')
            }
        },

        // Documentation
        jsdoc: {
            dist: {
                src: [
                    'static/scripts/*.js'
                ],
                options: {
                    destination: 'docs',
                    template: 'node_modules/minami'
                }
            }

        },

        // watch task
        watch: {
            less: {
                files: '/static/styles/*.less',
                tasks: ['less']
            }
        }

    });
    
    grunt.loadNpmTasks('grunt-jsdoc');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');
};
