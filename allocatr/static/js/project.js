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

window.transactionTableData = function () {
    return {
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
        paginationDisplay: "",
        updatePaginationDisplay() {
            var total = this.transactionList.size();
            var matching = this.transactionList.matchingItems.length;
            var firstShownItem = this.transactionList.i;
            if (total === 0) {
                this.paginationDisplay = "No transactions";
                return;
            } else if (this.transactionList.searched || this.transactionList.filtered) {
                if (matching === 0) {
                    this.paginationDisplay = "No matching transactions";
                    return;
                } else if (matching === 1) {
                    this.paginationDisplay = `Showing&nbsp;<span class="pagination-pill">1</span>&nbsp;transaction&nbsp;(filtered&nbsp;from&nbsp;${total})`;
                    return;
                } else {
                    var lastShownItem = firstShownItem + this.transactionList.visibleItems.length - 1;
                    this.paginationDisplay = `Showing&nbsp;<span class="pagination-pill">${firstShownItem}&nbsp;to&nbsp;${lastShownItem}</span>&nbsp;of&nbsp;${matching}&nbsp;transactions&nbsp;(filtered&nbsp;from&nbsp;${total})`;
                    return;
                }

            } else {
                if (total === 1) {
                    this.paginationDisplay = `Showing&nbsp;<span class="pagination-pill">1</span>&nbsp;transaction&nbsp;of&nbsp;${total}&nbsp;transactions`;
                    return;
                } else {
                    var lastShownItem = firstShownItem + this.transactionList.visibleItems.length - 1;
                    this.paginationDisplay = `Showing&nbsp;<span class="pagination-pill">${firstShownItem}&nbsp;to&nbsp;${lastShownItem}</span>&nbsp;of&nbsp;${total}&nbsp;transactions`;
                    return;
                }
            }
        },
        sortingState: {
            trType: "unsorted",
            trTitle: "unsorted",
            trCategory: "unsorted",
            trAmount: "unsorted",
            trAccount: "unsorted",
            trDate: "unsorted",
        },
        sortByColumn(column) {
            Object.keys(this.sortingState).forEach(key => {
                if (key === column) {
                    this.sortingState[key] = this.sortingState[key] === "asc" ? "desc" : "asc";
                } else {
                    this.sortingState[key] = "unsorted";
                }
            });
        },
    }
}

var sidebar = document.getElementById("sidebar");
var previousPeriodButton = document.getElementById("previous-period-button");
var nextPeriodButton = document.getElementById("next-period-button");

sidebar.addEventListener("reload-context", function () {
    setTimeout(function () {
        if (window.location.pathname === "/") {
            previousPeriodButton.classList.add("hidden");
            nextPeriodButton.classList.add("hidden");
        } else {
            previousPeriodButton.classList.remove("hidden");
            nextPeriodButton.classList.remove("hidden");
        }
    }, 750);
});
