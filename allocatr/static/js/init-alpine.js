function data() {
  return {
    // Side Menu
    isSideMenuOpen: false,
    toggleSideMenu() {
      this.isSideMenuOpen = !this.isSideMenuOpen
    },
    closeSideMenu() {
      this.isSideMenuOpen = false
    },

    // Profile Menu
    isProfileMenuOpen: false,
    toggleProfileMenu() {
      this.isProfileMenuOpen = !this.isProfileMenuOpen
    },
    closeProfileMenu() {
      this.isProfileMenuOpen = false
    },

    // Add Menu
    isAddMenuOpen: false,
    toggleAddMenu() {
      this.isAddMenuOpen = !this.isAddMenuOpen
    },
    closeAddMenu() {
      this.isAddMenuOpen = false
    },

    // Mobile Add Menu
    isMobileAddMenuOpen: false,
    toggleMobileAddMenu() {
      this.isMobileAddMenuOpen = !this.isMobileAddMenuOpen
    },
    closeMobileAddMenu() {
      this.isMobileAddMenuOpen = false
    },

    // Transaction Menu
    isTransactionsMenuOpen: false,
    toggleTransactionsMenu() {
      this.isTransactionsMenuOpen = !this.isTransactionsMenuOpen
    },


    // Modal
    isModalOpen: false,
    isStickyModalOpen: false,
    trapCleanup: null,
    openModal() {
      this.isModalOpen = true
      this.trapCleanup = focusTrap(document.querySelector('#modal'))
    },
    closeModal() {
      this.isModalOpen = false
      this.trapCleanup()
    },
    openStickyModal() {
      this.isStickyModalOpen = true
    },
    closeStickyModal() {
      this.isStickyModalOpen = false
    },

    // Transaction Modal
    openAddTransactionModal() {
      this.isAddMenuOpen = false
      this.openModal()
    },

    // Period
    firstDay: "",
    lastDay: "",
    period: {},
    periodDisplay: "",
    getPeriodDisplay(firstDay, lastDay) {
      const language = document.documentElement.lang;
      const now = new Date();
      const firstDayDate = new Date(firstDay);
      const lastDayDate = new Date(lastDay);
      const firstDayDayOfMonth = firstDayDate.toLocaleString(language, { day: "numeric" });

      if (now.getFullYear() === firstDayDate.getFullYear()) {
        if (firstDayDayOfMonth === "1") {
          return firstDayDate.toLocaleString(language, { month: "long" });
        } else {
          const firstDayMonthName = firstDayDate.toLocaleString(language, { month: "short" }).replace(/\./g, "");
          const lastDayMonthName = lastDayDate.toLocaleString(language, { month: "short" }).replace(/\./g, "");
          const lastDayDayOfMonth = lastDayDate.toLocaleString(language, { day: "numeric" });
          return `${firstDayDayOfMonth} ${firstDayMonthName} - ${lastDayDayOfMonth} ${lastDayMonthName}`;
        }
      } else {
        if (firstDayDayOfMonth === "1") {
          const monthName = firstDayDate.toLocaleString(language, { month: "long" });
          const year = firstDayDate.getFullYear();
          return `${monthName} ${year}`
        } else {
          const firstDayMonthName = firstDayDate.toLocaleString(language, { month: "short" }).replace(/\./g, "");
          const lastDayMonthName = lastDayDate.toLocaleString(language, { month: "short" }).replace(/\./g, "");
          const lastDayDayOfMonth = lastDayDate.toLocaleString(language, { day: "numeric" });
          const firstDayYear = firstDayDate.getFullYear()
          const lastDayYear = lastDayDate.getFullYear()
          if (firstDayYear === lastDayYear) {
            return `${firstDayDayOfMonth} ${firstDayMonthName} - ${lastDayDayOfMonth} ${lastDayMonthName} ${firstDayYear}`;
          } else {

            return `${firstDayDayOfMonth} ${firstDayMonthName} ${firstDayYear.toString().slice(-2)} - ${lastDayDayOfMonth} ${lastDayMonthName} ${lastDayYear.toString().slice(-2)}`;
          }
        }
      }
    },
    getHtmxPeriodVals() {
      const obj = {
        firstPeriodDay: this.period.firstDay,
        lastPeriodDay: this.period.lastDay
      }
      return JSON.stringify(obj)
    },
    getSelectedMonth() {
      return JSON.stringify({ month: this.period.month })
    },
    baseUrl: window.location.origin,
    async getAndSetCurrentPeriod() {
      this.period = await (await fetch(`${this.baseUrl}/current-month/`)).json();
      this.periodDisplay = this.getPeriodDisplay(this.period.firstDay, this.period.lastDay);
    },
    async getAndSetPreviousPeriod() {
      this.period = await (await fetch(`${this.baseUrl}/previous-month/${this.period.month}/`)).json();
      this.periodDisplay = this.getPeriodDisplay(this.period.firstDay, this.period.lastDay);
    },
    async getAndSetNextPeriod() {
      this.period = await (await fetch(`${this.baseUrl}/next-month/${this.period.month}/`)).json();
      this.periodDisplay = this.getPeriodDisplay(this.period.firstDay, this.period.lastDay);
    },
    getContext() {
      const current_page = window.location.pathname;
      if (current_page === '/') {
        return { transactionsContext: true, accountsContext: false, categoriesContext: false, budgetsContext: false }
      } else if (current_page.startsWith('/accounts/')) {
        return { transactionsContext: false, accountsContext: true, categoriesContext: false, budgetsContext: false }
      } else if (current_page.startsWith('/categories/')) {
        return { transactionsContext: false, accountsContext: false, categoriesContext: true, budgetsContext: false }
      } else if (current_page.startsWith('/budgets/')) {
        return { transactionsContext: false, accountsContext: false, categoriesContext: false, budgetsContext: true }
      }
    },
    updateChart(chart, labels, data) {
      console.log('updateChart function was called')
      chart.data.labels = labels;
      chart.data.datasets = [{ data: data }];
      chart.update();
    }
  }
}
