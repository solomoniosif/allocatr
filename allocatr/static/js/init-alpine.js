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
    trapCleanup: null,
    openModal() {
      this.isModalOpen = true
      document.querySelector('#modal').innerHTML = ''
      this.trapCleanup = focusTrap(document.querySelector('#modal'))
    },
    closeModal() {
      this.isModalOpen = false
      this.trapCleanup()
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
          const firstDayMonthName = firstDayDate.toLocaleString(language, { month: "short" });
          const lastDayMonthName = lastDayDate.toLocaleString(language, { month: "short" });
          const lastDayDayOfMonth = lastDayDate.toLocaleString(language, { day: "numeric" });
          return `${firstDayDayOfMonth} ${firstDayMonthName} - ${lastDayDayOfMonth} ${lastDayMonthName}`;
        }
      } else {
        if (firstDayDayOfMonth === "1") {
          const monthName = firstDayDate.toLocaleString(language, { month: "long" });
          const year = firstDayDate.getFullYear();
          return `${monthName} ${year}`
        } else {
          const firstDayMonthName = firstDayDate.toLocaleString(language, { month: "short" });
          const lastDayMonthName = lastDayDate.toLocaleString(language, { month: "short" });
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
    baseUrl: window.location.origin,
    async getAndSetCurrentPeriod() {
      this.period = await (await fetch(`${this.baseUrl}/current-period/`)).json();
      this.periodDisplay = this.getPeriodDisplay(this.period.firstDay, this.period.lastDay);
    },
    async getAndSetPreviousPeriod() {
      this.period = await (await fetch(`${this.baseUrl}/previous-period/${this.period.firstDay}/`)).json();
      this.periodDisplay = this.getPeriodDisplay(this.period.firstDay, this.period.lastDay);
    },
    async getAndSetNextPeriod() {
      this.period = await (await fetch(`${this.baseUrl}/next-period/${this.period.lastDay}/`)).json();
      this.periodDisplay = this.getPeriodDisplay(this.period.firstDay, this.period.lastDay);
    },
  }
}
