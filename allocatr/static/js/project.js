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
        toast.addEventListener('click', Swal.close)
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

window.allTransactionsList = function () {
    return {
        sortMenuOpen: false,
        filterMenuOpen: false,
        transactionList: new List('transactions-table', {
            valueNames: ['tr__type', 'tr__category', 'tr__title', 'tr__amount', 'tr__account', 'tr__date'],
            page: 10,
            pagination: true
        }),
        activeFilter: false,
        filterIncome() {
            this.activeFilter = true;
            this.transactionList.filter(function (tr) {
                if (tr.values().tr__type.includes("#income-icon")) {
                    return true;
                } else {
                    return false;
                }
            });
        },
        filterExpenses() {
            this.activeFilter = true;
            this.transactionList.filter(function (tr) {
                if (tr.values().tr__type.includes("#expense-icon")) {
                    return true;
                } else {
                    return false;
                }
            });
        },
        filterTransfers() {
            this.activeFilter = true;
            this.transactionList.filter(function (tr) {
                if (tr.values().tr__type.includes("#transfer-icon")) {
                    return true;
                } else {
                    return false;
                }
            })
        },
        removeFilters() {
            this.activeFilter = false;
            this.transactionList.filter();
        },
        searched: false,
        updateSearched() {
            this.searched = this.transactionList.searched;
        },
        listDisplay: "",
        updateListDisplay() {
            if (this.transactionList.searched || this.transactionList.filtered) {
                let visible = this.transactionList.visibleItems.length;
                let total = this.transactionList.matchingItems.length;
                this.listDisplay = `Showing&nbsp;<span class="pagination-pill">${visible}&nbsp;of&nbsp;${total}</span>&nbsp;<span class="text-red-500">filtered</span>&nbsp;transactions`;
            } else {
                let visible = this.transactionList.visibleItems.length;
                let total = this.transactionList.size();
                this.listDisplay = `Showing&nbsp;<span class="pagination-pill">${visible}&nbsp;of&nbsp;${total}</span>&nbsp;transactions`;
            }
        },
    }
}
