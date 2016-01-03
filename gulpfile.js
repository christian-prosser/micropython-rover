var gulp = require('gulp')
    ;

var micropython_drive = 'F:/'
    , sd_dir = micropython_drive
    ;

function plum_src() {
    var plumber = require('gulp-plumber'),
        notify = require('gulp-notify');

    return gulp.src.apply(this, arguments)
        .pipe(plumber({errorHandler: notify.onError("Error: <%= error.message %>")}));
}

gulp.task('sd', function () {
    return plum_src('sd/**/*')
        .pipe(gulp.dest(sd_dir))
});

gulp.task('clean', function (cb) {
    var del = require('del');
    return del([sd_dir], cb)
});

gulp.task('default', function () {
    gulp.start(
        'sd'
    );
});

gulp.task('watch', ['default'], function () {
    gulp.watch('sd/**/*.py', ['sd']);
});
