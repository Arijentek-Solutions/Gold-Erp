var m = (s, i, r) =>
	new Promise((t, e) => {
		var o = (a) => {
				try {
					c(r.next(a));
				} catch (p) {
					e(p);
				}
			},
			n = (a) => {
				try {
					c(r.throw(a));
				} catch (p) {
					e(p);
				}
			},
			c = (a) => (a.done ? t(a.value) : Promise.resolve(a.value).then(o, n));
		c((r = r.apply(s, i)).next());
	});
import {
	c as _,
	a as h,
	_ as g,
	b as v,
	r as y,
	o as L,
	d as E,
	e as A,
	s as P,
	f as w,
	g as k,
	h as O,
} from "./vendor.b4720657.js";
const R = function () {
	const i = document.createElement("link").relList;
	if (i && i.supports && i.supports("modulepreload")) return;
	for (const e of document.querySelectorAll('link[rel="modulepreload"]')) t(e);
	new MutationObserver((e) => {
		for (const o of e)
			if (o.type === "childList")
				for (const n of o.addedNodes)
					n.tagName === "LINK" && n.rel === "modulepreload" && t(n);
	}).observe(document, { childList: !0, subtree: !0 });
	function r(e) {
		const o = {};
		return (
			e.integrity && (o.integrity = e.integrity),
			e.referrerpolicy && (o.referrerPolicy = e.referrerpolicy),
			e.crossorigin === "use-credentials"
				? (o.credentials = "include")
				: e.crossorigin === "anonymous"
				? (o.credentials = "omit")
				: (o.credentials = "same-origin"),
			o
		);
	}
	function t(e) {
		if (e.ep) return;
		e.ep = !0;
		const o = r(e);
		fetch(e.href, o);
	}
};
R();
const b = "modulepreload",
	f = {},
	C = "/assets/zevar_core/pos/",
	u = function (i, r) {
		return !r || r.length === 0
			? i()
			: Promise.all(
					r.map((t) => {
						if (((t = `${C}${t}`), t in f)) return;
						f[t] = !0;
						const e = t.endsWith(".css"),
							o = e ? '[rel="stylesheet"]' : "";
						if (document.querySelector(`link[href="${t}"]${o}`)) return;
						const n = document.createElement("link");
						if (
							((n.rel = e ? "stylesheet" : b),
							e || ((n.as = "script"), (n.crossOrigin = "")),
							(n.href = t),
							document.head.appendChild(n),
							e)
						)
							return new Promise((c, a) => {
								n.addEventListener("load", c), n.addEventListener("error", a);
							});
					})
			  ).then(() => i());
	},
	j = [
		{
			path: "/login",
			name: "Login",
			component: () =>
				u(
					() => import("./Login.f856ccc9.js"),
					[
						"assets/Login.f856ccc9.js",
						"assets/vendor.b4720657.js",
						"assets/vendor.1875b906.css",
					]
				),
			meta: { guest: !0 },
		},
		{
			path: "/",
			name: "POS",
			component: () =>
				u(
					() => import("./POS.3b12f99a.js"),
					[
						"assets/POS.3b12f99a.js",
						"assets/POS.6acd6dca.css",
						"assets/AppLayout.0fa9b760.js",
						"assets/AppLayout.4b990617.css",
						"assets/vendor.b4720657.js",
						"assets/vendor.1875b906.css",
						"assets/ui.7e64e684.js",
					]
				),
			meta: { requiresAuth: !0 },
		},
		{
			path: "/catalogues",
			name: "Catalogues",
			component: () =>
				u(
					() => import("./CatalogueDashboard.c43729a4.js"),
					[
						"assets/CatalogueDashboard.c43729a4.js",
						"assets/CatalogueDashboard.e6a89a91.css",
						"assets/vendor.b4720657.js",
						"assets/vendor.1875b906.css",
						"assets/ui.7e64e684.js",
						"assets/ProductModal.47c14e3f.js",
						"assets/ProductModal.0aff546c.css",
					]
				),
			meta: { requiresAuth: !0 },
		},
		{
			path: "/catalogues/:category",
			name: "CategoryListing",
			component: () =>
				u(
					() => import("./CategoryListing.8e915287.js"),
					[
						"assets/CategoryListing.8e915287.js",
						"assets/CategoryListing.95a85314.css",
						"assets/vendor.b4720657.js",
						"assets/vendor.1875b906.css",
						"assets/ProductModal.47c14e3f.js",
						"assets/ProductModal.0aff546c.css",
						"assets/ui.7e64e684.js",
					]
				),
			meta: { requiresAuth: !0 },
		},
		{
			path: "/repairs",
			name: "Repairs",
			component: () =>
				u(
					() => import("./RepairTerminal.c24848e8.js"),
					[
						"assets/RepairTerminal.c24848e8.js",
						"assets/vendor.b4720657.js",
						"assets/vendor.1875b906.css",
						"assets/AppLayout.0fa9b760.js",
						"assets/AppLayout.4b990617.css",
						"assets/ui.7e64e684.js",
					]
				),
			meta: { requiresAuth: !0 },
		},
		{ path: "/:pathMatch(.*)*", redirect: "/" },
	],
	d = _({ history: h("/pos"), routes: j });
d.beforeEach((s, i, r) =>
	m(void 0, null, function* () {
		if (s.meta.guest) return r();
		if (s.meta.requiresAuth)
			try {
				const t = yield fetch("/api/method/frappe.auth.get_logged_user", {
					headers: { "X-Frappe-CSRF-Token": window.csrf_token || "" },
				});
				if (!t.ok) throw new Error("Not authenticated");
				const e = yield t.json();
				if (!e.message || e.message === "Guest") return r({ name: "Login" });
			} catch (t) {
				return r({ name: "Login" });
			}
		r();
	})
);
const q = {};
function S(s, i) {
	const r = y("router-view");
	return L(), v(r);
}
var T = g(q, [["render", S]]);
const l = E(T),
	D = A();
P("resourceFetcher", O);
l.use(D);
l.use(d);
l.use(w);
l.component("Button", k);
l.mount("#app");
"serviceWorker" in navigator &&
	window.addEventListener("load", () => {
		navigator.serviceWorker
			.register("/sw.js")
			.then((s) => {
				console.log("[App] Service Worker registered:", s.scope);
			})
			.catch((s) => {
				console.error("[App] Service Worker registration failed:", s);
			});
	});
