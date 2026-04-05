import { ApiError, DefaultService, OpenAPI } from '@/client'
import router from '@/router'
import { useTokenStore } from '@/stores/TokenStore'
import { useUserStore } from '@/stores/UserStore'
import { Notify } from 'quasar'

class AuthService {
  async update_user_info() {
    const userStore = useUserStore()

    // 获取用户
    const userResponse = await DefaultService.readCurrentUserUsersMeGet()
    // 保存用户
    userStore.saveUser(userResponse.user)
  }

  async login(username: string, password: string) {
    const tokenStore = useTokenStore()

    // 获取令牌
    const tokenResponse = await DefaultService.loginForAccessTokenTokenPost({
      username: username,
      password: password
    })

    // 将令牌保存到 tokenStorage
    tokenStore.saveToken(tokenResponse.access_token)
    // 在客户端保存令牌
    OpenAPI.TOKEN = tokenResponse.access_token

    await this.update_user_info()

    router.push({ path: '/' })
  }

  logout() {
    const userStore = useUserStore()
    const tokenStore = useTokenStore()

    userStore.removeUser()
    tokenStore.removeToken()
    OpenAPI.TOKEN = undefined
  }
}

export default new AuthService()
