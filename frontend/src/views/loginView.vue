<script setup>
import { nextTick, onMounted, ref } from "vue";
import { useAuthStore } from "../stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

const GOOGLE_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

const status = ref("loading");
const errorText = ref("");

function waitForGoogle() {
  return new Promise((resolve, reject) => {
    let tries = 0;

    const timer = setInterval(() => {
      tries += 1;

      if (window.google?.accounts?.id) {
        clearInterval(timer);
        resolve(true);
      }

      if (tries > 50) {
        clearInterval(timer);
        reject(new Error("Google script not loaded"));
      }
    }, 100);
  });
}

async function handleCredentialResponse(response) {
  errorText.value = "";
  try {
    const idToken = response.credential;
    await auth.loginWithGoogle(idToken);
    router.push("/dashboard");
  } catch (err) {
    console.error("Loggin error", err);
    errorText.value = "access denied. use corporate email.";
  }
}

onMounted(async () => {
  try {
    await waitForGoogle();

    if (!GOOGLE_ID) {
      status.value = "error";
      errorText.value = "google client id is missing (.env.local)";
      return;
    }

    window.google.accounts.id.initialize({
      client_id: GOOGLE_ID,
      callback: handleCredentialResponse,
    });

    window.google.accounts.id.renderButton(
      document.getElementById("googleBtn"),
      {
        theme: "outline",
        size: "large",
        shape: "pill",
        width: 320,
      },
    );

    status.value = "ready";
  } catch (e) {
    console.error(e);
    status.value = "error";
    errorText.value =
      "не вдалося завантажити google login. перевір інтернет або client id.";
  }
});
</script>

<template>
  <div class="page">
    <div class="card">
      <div class="brand">
        <div class="logo">
          <img src="/collage-logo.png" alt="Collage log" />
        </div>
        <div>
          <div class="title">EduTracker</div>
          <div class="subtitle">вхід тільки через корпоративну пошту</div>
        </div>
      </div>

      <div class="divider"></div>

      <div class="content">
        <div class="headline">sign in</div>
        <div class="hint">
          використай google аккаунт компанії, щоб переглянути навантаження
          викладачів.
        </div>

        <div class="authSlot">
          <div id="googleBtn" class="google"></div>
        </div>

        <div v-if="errorText" class="error">
          {{ errorText }}
        </div>

        <div class="footnote">
          продовжуючи, ти підтверджуєш доступ до внутрішнього сервісу.
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 80px 20px;
}

.card {
  width: 100%;
  max-width: 520px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 42px 36px;
  backdrop-filter: blur(12px);
  box-shadow: 0 30px 100px rgba(0, 0, 0, 0.6);
  animation: fadeIn 0.5s ease;
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 18px;
}

.logo {
  width: 46px;
  height: 46px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.logo img {
  max-width: 70%;
  max-height: 70%;
  object-fit: contain;
}

.title {
  font-weight: 700;
  font-size: 18px;
}

.subtitle {
  font-size: 13px;
  opacity: 0.7;
}

.divider {
  height: 1px;
  margin: 26px 0;
  background: rgba(255, 255, 255, 0.08);
}

.headline {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 12px;
}

.hint {
  opacity: 0.75;
  line-height: 1.6;
  margin-bottom: 26px;
}

.authSlot {
  margin-top: 18px;
  margin-bottom: 14px;

  min-height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.google {
  display: flex;
  justify-content: center;
}

.footnote {
  font-size: 12px;
  opacity: 0.55;
  text-align: center;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error {
  margin-top: 16px;
  padding: 12px 12px;
  border-radius: 14px;
  background: rgba(255, 77, 77, 0.08);
  border: 1px solid rgba(255, 77, 77, 0.22);
  color: rgba(255, 200, 200, 0.95);
}
</style>
