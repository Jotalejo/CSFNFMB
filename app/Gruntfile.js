module.exports = function(grunt) {
    grunt.initConfig({
		sass: {			
            dist: {
				options: {
					outputStyle: 'compressed'
				},
                files: [{
                    'static/assets/css/main.css':              'static/assets/scss/main.scss', 	                        /* 'All main SCSS' */

                    'static/assets/css/default.css':           'static/assets/scss/skins/default.scss',                   /* 'Theme SCSS to css path' */
                    'static/assets/css/dark.css':              'static/assets/scss/skins/dark.scss',                      /* 'Theme SCSS to css path' */

                    'static/assets/css/theme1.css':            'static/assets/scss/skins/theme1.scss',                    /* 'Theme SCSS to css path' */                    
                    'static/assets/css/theme2.css':            'static/assets/scss/skins/theme2.scss',                    /* 'Theme SCSS to css path' */                    
                    'static/assets/css/theme3.css':            'static/assets/scss/skins/theme3.scss',                    /* 'Theme SCSS to css path' */
                    'static/assets/css/theme4.css':            'static/assets/scss/skins/theme4.scss',                    /* 'Theme SCSS to css path' */
				}]
            }
        },  
        uglify: {
            my_target: {
              files: {
                    'static/assets/bundles/lib.vendor.bundle.js':   ['static/assets/plugins/jquery/jquery-3.4.1.min.js','static/assets/plugins/bootstrap/js/bootstrap.bundle.min.js','static/assets/plugins/metisMenu/metisMenu.js','static/assets/plugins/sparkline/sparkline.js','static/assets/js/vendors/circle-progress.min.js','static/assets/plugins/listjs/list.js'], /* main js*/
                    
                    /* 'assets/bundles/mainscripts.bundle.js':  ['assets/js/core.js'], /*coman js*/

                    'static/assets/bundles/counterup.bundle.js':           ['static/assets/plugins/counterjs/jquery.waypoints.js', 'static/assets/plugins/counterjs/jquery.counterup.min.js'],

                    'static/assets/bundles/c3.bundle.js':           ['static/assets/plugins/charts-c3/c3.min.js', 'static/assets/plugins/charts-c3/d3.v3.min.js'],
                    'static/assets/bundles/fullcalendar.bundle.js': ['static/assets/plugins/fullcalendar/moment.min.js', 'static/assets/plugins/fullcalendar/fullcalendar.min.js'],
                    'static/assets/bundles/summernote.bundle.js':   ['static/assets/plugins/summernote/dist/summernote.js'],
                    'static/assets/bundles/sweetalert.bundle.js':   ['static/assets/plugins/sweetalert/sweetalert.min.js'],
                    'static/assets/bundles/nestable.bundle.js':     ['static/assets/plugins/nestable/jquery.nestable.js'],
                    'static/assets/bundles/markdown.bundle.js':     ['static/assets/plugins/markdown/markdown.js','static/assets/plugins/markdown/to-markdown.js','static/assets/plugins/markdown/bootstrap-markdown.js'],
                    
                    'static/assets/bundles/flot.bundle.js':         ['static/assets/plugins/flot-charts/flot.js','static/assets/plugins/flot-charts/flot.resize.js','static/assets/plugins/flot-charts/flot.pie.js','static/assets/plugins/flot-charts/flot.categories.js','static/assets/plugins/flot-charts/flot.time.js'],
                    'static/assets/bundles/knobjs.bundle.js':       ['static/assets/plugins/knobjs/knob.min.js'],
                    'static/assets/bundles/echarts.bundle.js':      ['static/assets/plugins/echart/echarts.min.js'],
                    'static/assets/bundles/apexcharts.bundle.js':   ['static/assets/plugins/apexcharts/apexcharts.min.js'],
                    
                    
                    'static/assets/bundles/jvectormap1.bundle.js':  ['static/assets/plugins/jvectormap/jvectormap-2.0.3.min.js','static/assets/plugins/jvectormap/jvectormap-world.js','static/assets/plugins/jvectormap/jvectormap-in.js','static/assets/plugins/jvectormap/jvectormap-us.js','static/assets/plugins/jvectormap/jvectormap-au.js','static/assets/plugins/jvectormap/jvectormap-uk.js'],
                    'static/assets/bundles/jvectormap2.bundle.js':  ['templates/assets/js/map/jquery-jvectormap-2.0.3.min.js', 'templates/assets/js/map/jquery-jvectormap-de-merc.js', 'templates/assets/js/map/jquery-jvectormap-world-mill.js'],
                    
                    'static/assets/bundles/selectize.bundle.js':    ['templates/assets/js/vendors/selectize.min.js'],                    
                    
                    'static/assets/bundles/dataTables.bundle.js':[
                        'static/assets/plugins/datatable/jquery.dataTables.min.js',
                        'static/assets/plugins/datatable/dataTables.bootstrap4.min.js',
                        'static/assets/plugins/datatable/buttons/dataTables.buttons.min.js',
                        'static/assets/plugins/datatable/buttons/buttons.bootstrap4.min.js',
                        'static/assets/plugins/datatable/buttons/buttons.colVis.min.js',
                        'static/assets/plugins/datatable/buttons/buttons.html5.min.js',
                        'static/assets/plugins/datatable/buttons/buttons.print.min.js'], /*chartist js*/
                  }
              }
          }                      
    });
    grunt.loadNpmTasks("grunt-sass");
    grunt.loadNpmTasks('grunt-contrib-uglify');
    
    grunt.registerTask("buildcss", ["sass"]);
    grunt.registerTask("buildjs", ["uglify"]);
};
