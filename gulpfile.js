var browserSync  = require('browser-sync').create();
var gulp         = require('gulp');

var sass         = require('gulp-sass');
var postcss      = require('gulp-postcss');
var sourcemaps   = require('gulp-sourcemaps');
var autoprefixer = require('autoprefixer');
var changed      = require('gulp-changed');
var imagemin     = require('gulp-imagemin');

var json         = require('./package.json');
var pkg_name     = json.name;
var path_root    = './' + pkg_name + '/';
var path_assets  = path_root + '/assets/';
var path_static  = path_root + '/static/';


gulp.task('sass', function () {
  return gulp.src(path_assets + '/scss/*.scss')
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: ['./node_modules/'],
      errLogToConsole: true,
      outputStyle: 'expanded'
    }).on('error', sass.logError))
    .pipe(postcss([ autoprefixer({ browsers: ['last 2 versions'] }) ]))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(path_static + '/css/'))
    .pipe(browserSync.stream({match: '**/*.css'}));
});

// Static Server + watching scss/html files
gulp.task('proxy', ['watch'], function() {
  browserSync.init({
    proxy: 'localhost:8000'
  });
});

gulp.task('images', function() {
   var src = path_assets + '/img/*.+(png|jpg|gif|svg)';
   var dst = path_static + '/img/';

   return gulp.src(src)
     .pipe(changed(dst))
     .pipe(imagemin())
     .pipe(gulp.dest(dst));
});

gulp.task('watch', ['sass'], function(){
  gulp.watch(path_assets + '/scss/*.scss', ['sass']);
  gulp.watch(path_assets + '/img/*', ['images']);
  gulp.watch(path_root + "/*/templates/**.html").on('change', browserSync.reload);
  // gulp.watch("app/*.html").on('change', browserSync.reload);
})
console.log(path_assets + '/scss/*.scss');
gulp.task('default', ['images', 'sass', 'proxy', 'watch']);
