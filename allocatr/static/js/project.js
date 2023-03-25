/* Project specific Javascript goes here. */
var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

// Change the icons inside the button based on previous settings
if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    themeToggleLightIcon.classList.remove('hidden');
} else {
    themeToggleDarkIcon.classList.remove('hidden');
}

var themeToggleBtn = document.getElementById('theme-toggle');

themeToggleBtn.addEventListener('click', function () {

    // toggle icons inside button
    themeToggleDarkIcon.classList.toggle('hidden');
    themeToggleLightIcon.classList.toggle('hidden');

    // if set via local storage previously
    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'light') {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }

        // if NOT set via local storage previously
    } else {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    }

});

const twSwal = Swal.mixin({
    customClass: {
        container: 'bg-gray-200 text-gray-800 dark:bg-gray-800 dark:text-white',
        popup: 'rounded-2xl shadow-lg bg-gray-200 text-gray-800 dark:bg-gray-800 dark:text-white',
        //   header: '...',
        //   title: '...',
        //   closeButton: '...',
        icon: '',
        //   image: '...',
        //   htmlContainer: '...',
        //   input: '...',
        //   inputLabel: '...',
        //   validationMessage: '...',
        actions: 'space-x-5',
        confirmButton: 'primaryBtn',
        //   denyButton: '...',
        cancelButton: 'secondaryBtn',
        //   loader: '...',
        //   footer: '....',
        //   timerProgressBar: '....'
    },
    buttonsStyling: false,
})
window.twSwal = twSwal

const successToast = Swal.mixin({
    toast: true,
    position: 'top',
    showConfirmButton: false,
    timer: 4000,
    timerProgressBar: true,
    iconColor: 'white',
    width: 400,
    customClass: {
        popup: 'success-toast',
        timerProgressBar: 'bg-white'

    },
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})
window.successToast = successToast

const errorToast = Swal.mixin({
    toast: true,
    position: 'top',
    showConfirmButton: false,
    timer: 4000,
    timerProgressBar: true,
    iconColor: 'white',
    width: 400,
    customClass: {
        popup: 'error-toast',
        timerProgressBar: 'bg-white'

    },
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})
window.errorToast = errorToast

const warningToast = Swal.mixin({
    toast: true,
    position: 'top',
    showConfirmButton: false,
    timer: 4000,
    timerProgressBar: true,
    iconColor: 'white',
    width: 400,
    customClass: {
        popup: 'warning-toast',
        timerProgressBar: 'bg-white'

    },
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})
window.warningToast = warningToast

function getSelectedMonth() {
    if (window.selectedMonth) {
        return window.selectedMonth
    } else {
        const now = new Date();
        const year = now.getFullYear();
        const yearShort = year.toString().slice(-2);
        const month = now.getMonth() + 1;
        const monthStr = month.toString().padStart(2, "0");
        return yearShort + monthStr;
    }
}
