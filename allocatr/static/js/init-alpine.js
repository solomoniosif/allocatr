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
    displayDate(isoStringDate) {
      const date = new Date(isoStringDate);
      const language = document.documentElement.lang;
      let shortMonthName = date.toLocaleString(language, { month: "short" });
      shortMonthName = shortMonthName.replace(/\./g, "");
      const day = date.toLocaleString(language, { day: "numeric" });

      // Only return the year if the difference in months between input date and now is more than or equal to 11
      const now = new Date();
      let diffMonth = (now.getTime() - date.getTime()) / 1000;
      diffMonth /= (60 * 60 * 24 * 7 * 4);
      diffMonth = Math.abs(Math.round(diffMonth))
      if (diffMonth < 11) {
        return `${day} ${shortMonthName}`
      } else {
        const fullYear = date.getFullYear();
        const shortYear = fullYear.toString().slice(-2);
        return `${day} ${shortMonthName} ${shortYear}`
      }
    },
    getPeriodDisplay(firstDay, lastDay) {
      const firstDayDisplay = this.displayDate(firstDay);
      const lastDayDisplay = this.displayDate(lastDay);
      return `${firstDayDisplay} - ${lastDayDisplay}`
    },
    getHtmxPeriodVals() {
      // {"firstPeriodDay": "2023-03-15", "lastPeriodDay": "2023-04-14" }
      const obj = {
        firstPeriodDay: this.period.firstDay,
        lastPeriodDay: this.period.lastDay
      }
      return JSON.stringify(obj)
    },
  }
}
