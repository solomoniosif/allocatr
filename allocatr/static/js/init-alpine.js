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
  }
}
