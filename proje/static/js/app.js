const $ = (id) => document.getElementById(id);

let currentUser = null;
let desks = [];
let myDesk = null;
let toastInstance = null;

const api = async (url, options = {}) => {
    const response = await fetch(url, {
        credentials: "same-origin",
        ...options,
        headers: {
            ...(options.body ? { "Content-Type": "application/json" } : {}),
            ...options.headers
        }
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.error || data.message || "Bir hata oluştu.");
    }

    return data;
};

function notify(message, type = "success") {
    $("toastMessage").textContent = message;
    $("appToast").className = `toast text-bg-${type}`;
    toastInstance.show();
}

function showAuthError(message) {
    $("authAlert").textContent = message;
    $("authAlert").className = "alert alert-danger";
}

function showLogin() {
    $("authView").classList.remove("d-none");
    $("appView").classList.add("d-none");
}

function showDashboard() {
    $("authView").classList.add("d-none");
    $("appView").classList.remove("d-none");

    $("welcomeName").textContent = currentUser.username;
    $("sidebarUsername").textContent = currentUser.username;
    $("sidebarRole").textContent =
        currentUser.role === "admin" ? "Administrator" : "Student";
    $("userAvatar").textContent = currentUser.username.charAt(0).toUpperCase();

    document.querySelectorAll(".admin-only").forEach(element => {
        element.classList.toggle("d-none", currentUser.role !== "admin");
    });

    $("todayDate").textContent = new Intl.DateTimeFormat("tr-TR", {
        day: "numeric",
        month: "long",
        year: "numeric"
    }).format(new Date());

    loadDashboard();
}

async function checkSession() {
    try {
        const data = await api("/api/auth/me");
        currentUser = data.user;
        showDashboard();
    } catch {
        showLogin();
    }
}

async function login(event) {
    event.preventDefault();

    const form = new FormData(event.target);

    try {
        await api("/api/auth/login", {
            method: "POST",
            body: JSON.stringify({
                username: form.get("username"),
                password: form.get("password")
            })
        });

        await checkSession();
        notify("Başarıyla giriş yaptın.");
    } catch (error) {
        showAuthError(error.message);
    }
}

async function register(event) {
    event.preventDefault();

    const form = new FormData(event.target);

    try {
        await api("/api/auth/register", {
            method: "POST",
            body: JSON.stringify({
                username: form.get("username"),
                email: form.get("email"),
                password: form.get("password")
            })
        });

        event.target.reset();
        $("loginTab").click();
        showAuthError("Hesabın oluşturuldu. Şimdi giriş yapabilirsin.");
        $("authAlert").className = "alert alert-success";
    } catch (error) {
        showAuthError(error.message);
    }
}

async function logout() {
    try {
        await api("/api/auth/logout", { method: "POST" });
        currentUser = null;
        showLogin();
        notify("Oturum kapatıldı.");
    } catch (error) {
        notify(error.message, "danger");
    }
}

async function loadDashboard() {
    try {
        const data = await api("/api/desks/");
        desks = data.desks || [];

        renderStats();
        renderDesks();
        renderMySession();

        if (currentUser.role === "admin") {
            renderAdminDesks();
        }
    } catch (error) {
        notify(error.message, "danger");
    }
}

function renderStats() {
    $("totalDesks").textContent = desks.length;
    $("availableDesks").textContent =
        desks.filter(d => d.status === "available").length;
    $("occupiedDesks").textContent =
        desks.filter(d => d.status === "occupied").length;
    $("breakDesks").textContent =
        desks.filter(d => d.status === "on_break").length;
}

function renderDesks() {
    const grid = $("deskGrid");
    grid.innerHTML = "";

    if (!desks.length) {
        grid.innerHTML = '<div class="loading-state">Henüz masa eklenmemiş.</div>';
        return;
    }

    desks.forEach(desk => {
        const isMine = myDesk && Number(myDesk.id) === Number(desk.id);
        const status = desk.status || "available";

        const labels = {
            available: "Boş",
            occupied: "Dolu",
            on_break: "Molada",
            inactive: "Kapalı"
        };

        const button = document.createElement("button");
        button.type = "button";
        button.className = `desk-tile ${isMine ? "selected" : ""}`;
        button.disabled = status !== "available" || Boolean(myDesk);

        const indicator = document.createElement("span");
        indicator.className = `desk-status ${status}`;

        const code = document.createElement("strong");
        code.textContent = desk.desk_code;

        const floor = document.createElement("small");
        floor.textContent = desk.floor || "Kat bilgisi yok";

        const state = document.createElement("small");
        state.textContent = isMine ? "Senin masan" : labels[status] || status;

        button.append(indicator, code, floor, state);

        if (status === "available" && !myDesk) {
            button.addEventListener("click", () => selectDesk(desk.id));
        }

        grid.appendChild(button);
    });
}

function renderMySession() {
    myDesk = desks.find(d =>
        Number(d.occupied_by) === Number(currentUser.id)
    ) || null;

    const container = $("sessionContent");

    if (!myDesk) {
        container.className = "session-empty";
        container.innerHTML = `
            <div class="empty-icon">⌂</div>
            <strong>Henüz masa seçmedin</strong>
            <p>Çalışma alanlarından boş bir masa seçerek başlayabilirsin.</p>
        `;

        $("breakBtn").disabled = true;
        $("resumeBtn").disabled = true;
        $("releaseBtn").disabled = true;
        return;
    }

    const onBreak = myDesk.status === "on_break";

    container.className = "session-info";
    container.innerHTML = `
        <small>SEÇİLİ ÇALIŞMA ALANI</small>
        <strong>${escapeHtml(myDesk.desk_code)}</strong>
        <small>${escapeHtml(myDesk.floor || "Kat bilgisi yok")}</small>
        <div class="mt-2">
            <span class="badge ${onBreak ? "text-bg-warning" : "text-bg-success"}">
                ${onBreak ? "Moladasın" : "Aktif kullanım"}
            </span>
        </div>
        ${onBreak && myDesk.break_expires_at
            ? `<small class="d-block mt-2">Mola bitişi: ${escapeHtml(myDesk.break_expires_at)}</small>`
            : ""}
    `;

    $("breakBtn").disabled = onBreak;
    $("resumeBtn").disabled = !onBreak;
    $("releaseBtn").disabled = onBreak;
}

function escapeHtml(value) {
    return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[char]);
}

async function selectDesk(id) {
    try {
        await api(`/api/desks/${id}/select`, { method: "POST" });
        notify("Masa başarıyla seçildi.");
        await loadDashboard();
    } catch (error) {
        notify(error.message, "danger");
        await loadDashboard();
    }
}

async function startBreak() {
    try {
        await api("/api/desks/break", { method: "POST" });
        notify("10 dakikalık molan başladı.");
        await loadDashboard();
    } catch (error) {
        notify(error.message, "danger");
    }
}

async function resumeBreak() {
    try {
        await api("/api/desks/break/resume", { method: "POST" });
        notify("Tekrar masana döndün.");
        await loadDashboard();
    } catch (error) {
        notify(error.message, "danger");
        await loadDashboard();
    }
}

async function releaseDesk() {
    try {
        const data = await api("/api/desks/release", { method: "POST" });
        notify(data.message || "Masa bırakıldı.");
        await loadDashboard();
    } catch (error) {
        notify(error.message, "danger");
    }
}

async function gateExit() {
    if (!confirm("Çıkış turnikesinden geçmek istiyor musun?")) return;

    try {
        const data = await api("/api/gate/exit", { method: "POST" });

        if (data.desk_released) {
            notify("Çıkış başarılı. Masan boşaltıldı.");
        } else {
            notify("Çıkış başarılı. Moladaki masan korunuyor.");
        }

        await loadDashboard();
    } catch (error) {
        notify(error.message, "danger");
    }
}

async function renderAdminDesks() {
    try {
        const data = await api("/api/admin/desks");
        const list = $("adminDeskList");
        list.innerHTML = "";

        (data.desks || []).forEach(desk => {
            const row = document.createElement("div");
            row.className = "admin-desk-row";

            const info = document.createElement("div");
            const name = document.createElement("strong");
            name.textContent = desk.desk_code;

            const detail = document.createElement("small");
            detail.textContent = desk.floor || "Kat belirtilmemiş";

            info.append(name, detail);

            const button = document.createElement("button");
            button.className = `btn btn-sm ${desk.is_active ? "btn-outline-danger" : "btn-outline-success"}`;
            button.textContent = desk.is_active ? "Kapat" : "Aç";
            button.addEventListener("click", () => toggleDesk(desk));

            row.append(info, button);
            list.appendChild(row);
        });
    } catch (error) {
        $("adminDeskList").textContent = error.message;
    }
}

async function addDesk(event) {
    event.preventDefault();

    const form = new FormData(event.target);

    try {
        await api("/api/admin/desks", {
            method: "POST",
            body: JSON.stringify({
                desk_code: form.get("desk_code"),
                floor: form.get("floor")
            })
        });

        event.target.reset();
        notify("Yeni masa eklendi.");
        await loadDashboard();
    } catch (error) {
        notify(error.message, "danger");
    }
}

async function toggleDesk(desk) {
    try {
        await api(`/api/admin/desks/${desk.id}`, {
            method: "PATCH",
            body: JSON.stringify({
                is_active: desk.is_active ? 0 : 1
            })
        });

        notify("Masa durumu güncellendi.");
        await loadDashboard();
    } catch (error) {
        notify(error.message, "danger");
    }
}

function initialize() {
    toastInstance = new bootstrap.Toast($("appToast"), { delay: 3000 });

    $("loginTab").addEventListener("click", () => {
        $("loginTab").classList.add("active");
        $("registerTab").classList.remove("active");
        $("loginForm").classList.remove("d-none");
        $("registerForm").classList.add("d-none");
        $("authAlert").classList.add("d-none");
    });

    $("registerTab").addEventListener("click", () => {
        $("registerTab").classList.add("active");
        $("loginTab").classList.remove("active");
        $("registerForm").classList.remove("d-none");
        $("loginForm").classList.add("d-none");
        $("authAlert").classList.add("d-none");
    });

    $("loginForm").addEventListener("submit", login);
    $("registerForm").addEventListener("submit", register);
    $("logoutBtn").addEventListener("click", logout);
    $("refreshBtn").addEventListener("click", loadDashboard);
    $("breakBtn").addEventListener("click", startBreak);
    $("resumeBtn").addEventListener("click", resumeBreak);
    $("releaseBtn").addEventListener("click", releaseDesk);
    $("gateExitBtn").addEventListener("click", gateExit);
    $("addDeskForm").addEventListener("submit", addDesk);

    $("footerYear").textContent = new Date().getFullYear();

    checkSession();

    // Masa durumlarını 10 saniyede bir yenile.
    setInterval(() => {
        if (currentUser) loadDashboard();
    }, 10000);
}

document.addEventListener("DOMContentLoaded", initialize);
