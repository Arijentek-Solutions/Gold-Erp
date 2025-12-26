import { reactive } from 'vue';
import { createResource } from 'frappe-ui';
import { useRouter } from 'vue-router';

export const session = reactive({
  user: null,
  isLoggedIn: false,
  
  // Resource to check login status
  userResource: createResource({
    url: 'frappe.auth.get_logged_user',
    onSuccess(data) {
      session.user = data;
      session.isLoggedIn = true;
    },
    onError() {
      session.user = null;
      session.isLoggedIn = false;
    }
  }),

  async fetch() {
    await this.userResource.submit();
  },

  async logout() {
    await createResource({ url: 'logout' }).submit();
    this.user = null;
    this.isLoggedIn = false;
    window.location.href = '/login'; 
  }
});