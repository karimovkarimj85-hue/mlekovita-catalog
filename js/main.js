const CATALOG = window.CATALOG || [];
const FAV_KEY = "mlekovita-favs";

const toggle = document.querySelector(".nav__toggle");
const menu = document.querySelector(".menu");
const form = document.getElementById("lead-form");
const grid = document.getElementById("catalog-grid");
const wipe = document.getElementById("wipe");

function favs() {
  try {
    return JSON.parse(localStorage.getItem(FAV_KEY) || "[]");
  } catch {
    return [];
  }
}

function setFavs(ids) {
  localStorage.setItem(FAV_KEY, JSON.stringify(ids));
}

function goTo(href) {
  if (!wipe || document.documentElement.classList.contains("is-phone")) {
    location.href = href;
    return;
  }
  wipe.classList.add("is-in");
  setTimeout(() => {
    location.href = href;
  }, 420);
}

function bindMenu() {
  if (!toggle || !menu) return;
  toggle.addEventListener("click", () => {
    const open = menu.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", String(open));
  });
  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      menu.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    });
  });
}

function bindForm() {
  if (!form) return;
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const lines = [
      "Здравствуйте! Заявка с каталога сливок Mlekovita.",
      `Имя: ${String(data.get("name") || "").trim()}`,
      data.get("company") ? `Компания: ${String(data.get("company")).trim()}` : "",
      `Телефон: ${String(data.get("phone") || "").trim()}`,
      data.get("message") ? `Комментарий: ${String(data.get("message")).trim()}` : "",
    ].filter(Boolean);
    window.open(`https://wa.me/998950160330?text=${encodeURIComponent(lines.join("\n"))}`, "_blank", "noopener");
  });
}

function cardHtml(item, index) {
  const saved = favs().includes(item.id);
  return `
    <article class="card reveal" data-kind="${item.kind}" data-tone="${item.tone}" style="--d:${index * 90}ms; --zoom:${item.zoom || 1}">
      <button class="fav ${saved ? "is-on" : ""}" type="button" data-fav="${item.id}" aria-label="В избранное">♥</button>
      <a class="card__media js-open" href="./product.html?id=${item.id}" data-href="./product.html?id=${item.id}">
        <img src="${item.image}" alt="${item.alt}" />
      </a>
      <div class="card__body">
        <h3><span class="card__name">Сливки </span>Mlekovita</h3>
        <p class="card__meta">${item.fat} · ${item.volume}</p>
        <span class="tag">${item.tag}</span>
        <div class="price">
          <strong>${item.price}</strong>
          <span>сум/шт <small>с НДС</small></span>
        </div>
        <a class="btn btn--gold btn--full js-open" href="./product.html?id=${item.id}" data-href="./product.html?id=${item.id}"><span class="btn__full">Подробнее</span><span class="btn__short">Ещё</span></a>
      </div>
    </article>
  `;
}

function renderCatalog(filter = "all") {
  if (!grid) return;
  const items = CATALOG.filter((item) => filter === "all" || item.kind === filter);
  grid.innerHTML = items.map(cardHtml).join("");
  observeReveal();
}

function bindFilters() {
  document.querySelectorAll(".chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      document.querySelectorAll(".chip").forEach((el) => el.classList.remove("is-active"));
      chip.classList.add("is-active");
      renderCatalog(chip.dataset.filter);
    });
  });
}

function bindFavs() {
  document.addEventListener("click", (event) => {
    const btn = event.target.closest("[data-fav]");
    if (!btn) return;
    event.preventDefault();
    const id = btn.dataset.fav;
    const next = new Set(favs());
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setFavs([...next]);
    btn.classList.toggle("is-on", next.has(id));
  });
}

function bindPageLinks() {
  document.addEventListener("click", (event) => {
    const link = event.target.closest(".js-open");
    if (!link) return;
    event.preventDefault();
    goTo(link.dataset.href || link.getAttribute("href"));
  });
}

function observeReveal() {
  const nodes = document.querySelectorAll(".reveal");
  if (!nodes.length) return;
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.16 }
  );
  nodes.forEach((node) => io.observe(node));
}

function renderProductPage() {
  const root = document.getElementById("product-page");
  if (!root) return;
  const id = new URLSearchParams(location.search).get("id");
  const item = CATALOG.find((entry) => entry.id === id);
  const empty = document.getElementById("product-empty");
  if (!item) {
    empty.hidden = false;
    return;
  }
  document.title = `${item.name} ${item.fat} ${item.volume} — Euro Brands Group`;
  const saved = favs().includes(item.id);
  const related = CATALOG.filter((entry) => entry.id !== item.id)
    .map(
      (entry) => `
        <a class="mini js-open" href="./product.html?id=${entry.id}" data-href="./product.html?id=${entry.id}">
          <img src="${entry.image}" alt="" />
          <span>${entry.fat} · ${entry.volume}</span>
        </a>
      `
    )
    .join("");

  root.insertAdjacentHTML(
    "beforeend",
    `
    <section class="pdp__grid">
      <figure class="shot-lg" data-tone="${item.tone}" style="--zoom:${item.zoom || 1}">
        <img src="${item.image}" alt="${item.alt}" />
      </figure>
      <div class="pdp__info">
        <span class="tag">${item.tag}</span>
        <h1>${item.name}</h1>
        <p class="pdp__spec">${item.fat} · ${item.volume}</p>
        <p class="pdp__lead">${item.lead}</p>
        <div class="price price--pdp">
          <strong>${item.price}</strong>
          <span>сум / шт<br />с НДС</span>
        </div>
        <ul class="pdp__list">
          ${item.features.map((line) => `<li>${line}</li>`).join("")}
        </ul>
        <div class="pdp__actions">
          <a class="btn btn--gold" href="https://wa.me/998950160330?text=${encodeURIComponent(
            `Здравствуйте! Интересуют ${item.name} ${item.fat}, ${item.volume}.`
          )}" target="_blank" rel="noopener">Заказать в WhatsApp</a>
          <button class="btn btn--ghost fav-btn ${saved ? "is-on" : ""}" type="button" data-fav="${item.id}">В избранное</button>
          <button class="btn btn--ghost" type="button" id="share-btn">Поделиться</button>
        </div>
      </div>
    </section>
    <section class="related">
      <h2>Другие позиции</h2>
      <div class="related__row">${related}</div>
    </section>
  `
  );

  document.getElementById("share-btn")?.addEventListener("click", async () => {
    const url = location.href;
    try {
      if (navigator.share) {
        await navigator.share({ title: document.title, url });
        return;
      }
      await navigator.clipboard.writeText(url);
    } catch {
      await navigator.clipboard.writeText(url);
    }
    const btn = document.getElementById("share-btn");
    btn.textContent = "Ссылка скопирована";
    setTimeout(() => (btn.textContent = "Поделиться"), 1600);
  });
}

function setupPhone() {
  if (!document.documentElement.classList.contains("is-phone")) return;
  document.body.classList.add("is-phone");
  document.querySelectorAll(".phone-pill").forEach((el) => {
    el.hidden = false;
  });

  if (!document.querySelector(".phone-dock")) {
    const onProduct = Boolean(document.getElementById("product-page"));
    const catalogHref = onProduct ? "./index.html#products" : "#products";
    document.body.insertAdjacentHTML(
      "beforeend",
      `
      <nav class="phone-dock" aria-label="Быстрые действия">
        <a href="${catalogHref}">Каталог</a>
        <a href="tel:+998950160330">Звонок</a>
        <a class="phone-dock__wa" href="https://wa.me/998950160330" target="_blank" rel="noopener">WhatsApp</a>
      </nav>
    `
    );
  }

  if (!sessionStorage.getItem("mlekovita-phone-hello") && !document.querySelector(".phone-toast")) {
    document.body.insertAdjacentHTML(
      "beforeend",
      `
      <div class="phone-toast" role="status">
        <p><strong>Вы открыли каталог с телефона.</strong> Листайте карточки, жмите «Подробнее» или сразу пишите в WhatsApp.</p>
        <button type="button" class="phone-toast__ok">Понятно</button>
      </div>
    `
    );
    const toast = document.querySelector(".phone-toast");
    const close = () => {
      toast?.classList.add("is-out");
      sessionStorage.setItem("mlekovita-phone-hello", "1");
      setTimeout(() => toast?.remove(), 280);
    };
    toast?.querySelector(".phone-toast__ok")?.addEventListener("click", close);
    setTimeout(close, 7000);
  }
}

bindMenu();
bindForm();
bindFavs();
bindPageLinks();
bindFilters();
renderCatalog();
renderProductPage();
observeReveal();
setupPhone();
