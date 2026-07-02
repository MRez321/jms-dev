import { onMounted, ref } from 'vue'
import { VueCookieNext as VueCookie } from 'vue-cookie-next'

const RTL_LANGUAGES = ['fa']

export function useRtl() {
  const currentLang = ref(null)
  let interval = null

  function updateDirection() {
    const lang = VueCookie.getCookie('django_language')
    // Default to LTR if no cookie or not RTL language
    const isRtl = RTL_LANGUAGES.includes(lang)
    document.documentElement.setAttribute('dir', isRtl ? 'rtl' : 'ltr')
  }

  onMounted(() => {
    // Set LTR immediately as default
    document.documentElement.setAttribute('dir', 'ltr')

    // Then check cookie and update
    updateDirection()

    // Poll briefly in case cookie loads late
    interval = setInterval(() => {
      const lang = VueCookie.getCookie('django_language')
      if (lang && lang !== currentLang.value) {
        currentLang.value = lang
        updateDirection()
      }
    }, 300)

    setTimeout(() => clearInterval(interval), 3000)
  })
}
