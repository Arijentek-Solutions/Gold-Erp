var E = (v, r, i) =>
	new Promise((c, h) => {
		var u = (a) => {
				try {
					l(i.next(a));
				} catch (x) {
					h(x);
				}
			},
			b = (a) => {
				try {
					l(i.throw(a));
				} catch (x) {
					h(x);
				}
			},
			l = (a) => (a.done ? c(a.value) : Promise.resolve(a.value).then(u, b));
		l((i = i.apply(v, r)).next());
	});
import {
	E as G,
	p as Q,
	i as C,
	j as T,
	_ as K,
	x as B,
	y as U,
	o,
	b as J,
	z as P,
	k as s,
	l as e,
	F as S,
	A as z,
	n as j,
	t as n,
	u as t,
	G as f,
	m as H,
	v as W,
	T as X,
	B as N,
	C as q,
	q as O,
	D as I,
	H as ee,
	r as te,
	I as oe,
	J as se,
	K as Y,
} from "./vendor.b4720657.js";
import { u as L, a as Z } from "./ui.3a424cc5.js";
const re = G("session", () => {
		const v = Q(),
			r = C(null),
			i = C(!1),
			c = C(localStorage.getItem("active_warehouse") || null),
			h = T({
				url: "frappe.auth.get_logged_user",
				auto: !0,
				onSuccess(l) {
					typeof l == "string" ? (r.value = { full_name: l, email: l }) : (r.value = l),
						(i.value = !0);
				},
				onError() {
					(r.value = null),
						(i.value = !1),
						window.location.pathname !== "/pos/login" && v.push("/login");
				},
			}),
			u = T({
				url: "logout",
				onSuccess() {
					(r.value = null),
						(i.value = !1),
						(c.value = null),
						localStorage.removeItem("active_warehouse"),
						(window.location.href = "/pos/login");
				},
			});
		function b(l) {
			(c.value = l),
				l
					? localStorage.setItem("active_warehouse", l)
					: localStorage.removeItem("active_warehouse");
		}
		return {
			user: r,
			isLoggedIn: i,
			currentWarehouse: c,
			userResource: h,
			logoutResource: u,
			setWarehouse: b,
		};
	}),
	ae = G("gold", () => {
		const v = C({}),
			r = C(null),
			i = T({
				url: "frappe.client.get_list",
				makeParams() {
					return {
						doctype: "Gold Rate Log",
						fields: ["metal", "purity", "rate_per_gram"],
						order_by: "timestamp desc",
						limit_page_length: 20,
					};
				},
				onSuccess(h) {
					const u = {};
					h.forEach((b) => {
						const l = `${b.metal}-${b.purity}`;
						u[l] || (u[l] = b.rate_per_gram);
					}),
						(v.value = u),
						(r.value = new Date());
				},
			});
		function c() {
			i.fetch(),
				setInterval(() => {
					i.fetch();
				}, 6e4);
		}
		return { rates: v, lastUpdated: r, startPolling: c };
	});
const y = (v) => (N("data-v-7900f27f"), (v = v()), q(), v),
	ne = { key: 0, class: "fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6" },
	le = {
		class: "w-full md:w-1/2 bg-gray-50 dark:bg-[#15171e] p-6 border-r border-gray-100 dark:border-white/5 flex flex-col",
	},
	ie = y(() =>
		e(
			"h3",
			{
				class: "text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-wider mb-4",
			},
			"Items in Bag",
			-1
		)
	),
	de = { class: "flex-1 overflow-y-auto space-y-3 pr-2 custom-scrollbar" },
	ce = { class: "flex items-center gap-3" },
	ue = {
		class: "w-10 h-10 bg-gray-100 dark:bg-gray-800 rounded-md overflow-hidden flex-shrink-0",
	},
	he = ["src"],
	xe = { class: "min-w-0" },
	ge = { class: "font-bold text-gray-900 dark:text-white text-sm line-clamp-1" },
	pe = { class: "text-xs text-gray-500 dark:text-gray-400 truncate" },
	be = { class: "text-right flex-shrink-0" },
	fe = { class: "font-mono font-bold text-sm text-gray-900 dark:text-gray-200" },
	ve = { class: "text-[10px] text-gray-400" },
	_e = { class: "mt-4 pt-4 border-t border-gray-200 dark:border-white/10" },
	ye = { class: "flex items-center justify-between cursor-pointer group" },
	me = y(() =>
		e(
			"div",
			null,
			[
				e("span", { class: "font-medium text-gray-700 dark:text-gray-300" }, "Tax Exempt"),
				e(
					"span",
					{ class: "text-xs text-gray-400 block" },
					"For resellers or tax-free sales"
				),
			],
			-1
		)
	),
	ke = { class: "mt-4 space-y-2 pt-4 border-t border-gray-200 dark:border-white/10" },
	we = { class: "flex justify-between text-sm text-gray-500 dark:text-gray-400" },
	$e = y(() => e("span", null, "Subtotal", -1)),
	Fe = {
		class: "flex justify-between text-2xl font-bold text-gray-900 dark:text-white pt-2 border-t border-gray-200 dark:border-white/10 mt-2",
	},
	Ce = y(() => e("span", null, "Total", -1)),
	je = {
		class: "w-full md:w-1/2 p-6 flex flex-col bg-white dark:bg-[#1a1c23] relative overflow-y-auto",
	},
	Se = y(() =>
		e(
			"svg",
			{
				class: "w-5 h-5 text-gray-400",
				fill: "none",
				viewBox: "0 0 24 24",
				stroke: "currentColor",
			},
			[
				e("path", {
					"stroke-linecap": "round",
					"stroke-linejoin": "round",
					"stroke-width": "2",
					d: "M6 18L18 6M6 6l12 12",
				}),
			],
			-1
		)
	),
	Ae = [Se],
	Me = y(() =>
		e("h2", { class: "text-xl font-bold text-gray-900 dark:text-white mb-1" }, "Payment", -1)
	),
	De = y(() =>
		e(
			"p",
			{ class: "text-sm text-gray-500 dark:text-gray-400 mb-4" },
			"Select payment method(s). Split payments allowed.",
			-1
		)
	),
	ze = { class: "space-y-2 mb-4" },
	Be = ["onClick"],
	Ie = { class: "flex items-center gap-3" },
	Ve = { key: 0, class: "w-4 h-4", fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
	Oe = y(() =>
		e(
			"path",
			{
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z",
			},
			null,
			-1
		)
	),
	Pe = [Oe],
	Te = { key: 1, class: "w-4 h-4", fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
	Re = y(() =>
		e(
			"path",
			{
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z",
			},
			null,
			-1
		)
	),
	He = [Re],
	Le = { class: "font-medium text-gray-900 dark:text-white text-sm" },
	Ee = { key: 0, class: "w-2 h-2 rounded-full bg-green-500" },
	Ge = {
		key: 0,
		class: "bg-gray-50 dark:bg-[#15171e] rounded-xl p-4 mb-4 border border-gray-100 dark:border-white/5",
	},
	Ke = y(() =>
		e(
			"h4",
			{ class: "text-xs font-bold text-gray-400 uppercase tracking-wider mb-3" },
			"Split Amounts",
			-1
		)
	),
	Ue = { class: "text-sm text-gray-600 dark:text-gray-300" },
	We = { class: "flex items-center gap-2" },
	Ne = y(() => e("span", { class: "text-gray-400" }, "$", -1)),
	qe = ["onUpdate:modelValue", "onInput", "max"],
	Ye = {
		class: "flex justify-between text-sm pt-2 border-t border-gray-200 dark:border-white/10 mt-2",
	},
	Ze = y(() => e("span", { class: "text-gray-500" }, "Remaining", -1)),
	Qe = { class: "mt-auto" },
	Je = ["disabled"],
	Xe = {
		key: 0,
		class: "animate-spin rounded-full h-5 w-5 border-2 border-gray-400 border-t-white",
	},
	et = { key: 1 },
	tt = { key: 2 },
	ot = {
		key: 1,
		class: "p-10 flex flex-col items-center justify-center text-center w-full bg-white dark:bg-[#1a1c23]",
	},
	st = y(() =>
		e(
			"div",
			{
				class: "w-20 h-20 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mb-6 animate-bounce-short",
			},
			[
				e(
					"svg",
					{
						class: "w-10 h-10 text-green-600 dark:text-green-400",
						fill: "none",
						stroke: "currentColor",
						viewBox: "0 0 24 24",
					},
					[
						e("path", {
							"stroke-linecap": "round",
							"stroke-linejoin": "round",
							"stroke-width": "2.5",
							d: "M5 13l4 4L19 7",
						}),
					]
				),
			],
			-1
		)
	),
	rt = y(() =>
		e(
			"h2",
			{ class: "text-2xl font-bold text-gray-900 dark:text-white mb-2" },
			"Payment Successful!",
			-1
		)
	),
	at = y(() =>
		e(
			"p",
			{ class: "text-gray-500 dark:text-gray-400 mb-8" },
			"Invoice has been generated in ERPNext.",
			-1
		)
	),
	nt = {
		class: "bg-gray-50 dark:bg-[#15171e] rounded-xl p-4 w-full mb-6 border border-gray-100 dark:border-white/5",
	},
	lt = { class: "flex justify-between text-sm mb-2" },
	it = y(() => e("span", { class: "text-gray-500 dark:text-gray-400" }, "Transaction ID", -1)),
	dt = { class: "font-mono font-bold text-gray-900 dark:text-white" },
	ct = { class: "flex justify-between text-sm" },
	ut = y(() => e("span", { class: "text-gray-500 dark:text-gray-400" }, "Amount Paid", -1)),
	ht = { class: "font-mono font-bold text-green-600 dark:text-green-400" },
	xt = {
		key: 0,
		class: "flex justify-between text-sm mt-2 pt-2 border-t border-gray-200 dark:border-white/10",
	},
	gt = y(() => e("span", { class: "text-gray-500 dark:text-gray-400" }, "Tax Status", -1)),
	pt = y(() => e("span", { class: "text-green-500 font-medium" }, "Exempt", -1)),
	bt = [gt, pt],
	ft = y(() =>
		e(
			"button",
			{
				class: "flex-1 py-3 rounded-lg font-bold text-white bg-gray-900 hover:bg-black dark:bg-[#D4AF37] dark:text-black dark:hover:bg-[#b5952f] transition flex items-center justify-center gap-2",
			},
			[
				e(
					"svg",
					{
						class: "w-4 h-4",
						fill: "none",
						stroke: "currentColor",
						viewBox: "0 0 24 24",
					},
					[
						e("path", {
							"stroke-linecap": "round",
							"stroke-linejoin": "round",
							"stroke-width": "2",
							d: "M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2-4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z",
						}),
					]
				),
				O(" Print Receipt "),
			],
			-1
		)
	),
	vt = {
		props: ["show"],
		emits: ["close"],
		setup(v, { emit: r }) {
			const i = v,
				c = L(),
				h = C(!1),
				u = C("review"),
				b = C(null),
				l = C(!1),
				a = C([]),
				x = [
					{ mode: "Cash", type: "Cash" },
					{ mode: "Credit Card", type: "Bank" },
					{ mode: "Debit Card", type: "Bank" },
					{ mode: "Check", type: "Bank" },
					{ mode: "Wire Transfer", type: "Bank" },
					{ mode: "Zelle", type: "Bank" },
				],
				d = B(() => (l.value ? c.subtotal : c.grandTotal)),
				$ = B(() => {
					const _ = a.value.reduce((D, g) => D + (g.amount || 0), 0);
					return d.value - _;
				}),
				F = B(() =>
					a.value.length === 0
						? !1
						: a.value.length === 1
						? !0
						: Math.abs($.value) < 0.01
				);
			function w(_) {
				return a.value.some((D) => D.mode === _);
			}
			function m(_) {
				const D = a.value.findIndex((g) => g.mode === _);
				D >= 0
					? a.value.splice(D, 1)
					: a.value.length === 0
					? a.value.push({ mode: _, amount: d.value })
					: a.value.push({ mode: _, amount: 0 });
			}
			function p(_) {}
			U(
				() => i.show,
				(_) => {
					_ && ((u.value = "review"), (a.value = []), (h.value = !1), (l.value = !1));
				}
			);
			function V() {
				return E(this, null, function* () {
					if (!!F.value) {
						h.value = !0;
						try {
							const _ = yield c.submitOrder(a.value, l.value);
							_ && _.data && _.data.name && (b.value = _.data.name),
								(u.value = "success");
						} catch (_) {
							alert("Order failed: " + _.message);
						} finally {
							h.value = !1;
						}
					}
				});
			}
			function k() {
				r("close"), u.value === "success" && c.clearCart();
			}
			function M(_) {
				return _
					? new Intl.NumberFormat("en-US", {
							style: "currency",
							currency: "USD",
					  }).format(_)
					: "$0.00";
			}
			return (_, D) => (
				o(),
				J(
					X,
					{ name: "fade" },
					{
						default: P(() => [
							v.show
								? (o(),
								  s("div", ne, [
										e("div", {
											onClick: k,
											class: "absolute inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity",
										}),
										e(
											"div",
											{
												class: f([
													"relative bg-white dark:bg-[#1a1c23] rounded-2xl shadow-2xl w-full overflow-hidden flex flex-col md:flex-row transition-all duration-500 ease-in-out border border-transparent dark:border-white/10",
													u.value === "success"
														? "max-w-md"
														: "max-w-4xl h-[650px]",
												]),
											},
											[
												u.value === "review"
													? (o(),
													  s(
															S,
															{ key: 0 },
															[
																e("div", le, [
																	ie,
																	e("div", de, [
																		(o(!0),
																		s(
																			S,
																			null,
																			z(
																				t(c).items,
																				(g) => (
																					o(),
																					s(
																						"div",
																						{
																							key: g.item_code,
																							class: "flex justify-between items-center bg-white dark:bg-[#0F1115] p-3 rounded-lg border border-gray-100 dark:border-white/5 shadow-sm",
																						},
																						[
																							e(
																								"div",
																								ce,
																								[
																									e(
																										"div",
																										ue,
																										[
																											g.image
																												? (o(),
																												  s(
																														"img",
																														{
																															key: 0,
																															src: g.image,
																															class: "w-full h-full object-cover",
																														},
																														null,
																														8,
																														he
																												  ))
																												: j(
																														"",
																														!0
																												  ),
																										]
																									),
																									e(
																										"div",
																										xe,
																										[
																											e(
																												"div",
																												ge,
																												n(
																													g.item_name
																												),
																												1
																											),
																											e(
																												"div",
																												pe,
																												n(
																													g.item_code
																												),
																												1
																											),
																										]
																									),
																								]
																							),
																							e(
																								"div",
																								be,
																								[
																									e(
																										"div",
																										fe,
																										n(
																											M(
																												g.amount *
																													g.qty
																											)
																										),
																										1
																									),
																									e(
																										"div",
																										ve,
																										"Qty: " +
																											n(
																												g.qty
																											),
																										1
																									),
																								]
																							),
																						]
																					)
																				)
																			),
																			128
																		)),
																	]),
																	e("div", _e, [
																		e("label", ye, [
																			me,
																			e(
																				"button",
																				{
																					onClick:
																						D[0] ||
																						(D[0] = (
																							g
																						) =>
																							(l.value =
																								!l.value)),
																					class: f([
																						"relative inline-flex h-6 w-11 items-center rounded-full transition-colors",
																						l.value
																							? "bg-green-500"
																							: "bg-gray-300 dark:bg-gray-600",
																					]),
																				},
																				[
																					e(
																						"span",
																						{
																							class: f(
																								[
																									"inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform",
																									l.value
																										? "translate-x-6"
																										: "translate-x-1",
																								]
																							),
																						},
																						null,
																						2
																					),
																				],
																				2
																			),
																		]),
																	]),
																	e("div", ke, [
																		e("div", we, [
																			$e,
																			e(
																				"span",
																				null,
																				n(
																					M(
																						t(c)
																							.subtotal
																					)
																				),
																				1
																			),
																		]),
																		e(
																			"div",
																			{
																				class: f([
																					"flex justify-between text-sm",
																					l.value
																						? "text-green-500 line-through"
																						: "text-gray-500 dark:text-gray-400",
																				]),
																			},
																			[
																				e(
																					"span",
																					null,
																					"Tax (" +
																						n(
																							l.value
																								? "0"
																								: t(
																										c
																								  )
																										.taxRate
																						) +
																						"%)",
																					1
																				),
																				e(
																					"span",
																					null,
																					n(
																						M(
																							l.value
																								? 0
																								: t(
																										c
																								  )
																										.tax
																						)
																					),
																					1
																				),
																			],
																			2
																		),
																		e("div", Fe, [
																			Ce,
																			e(
																				"span",
																				null,
																				n(M(t(d))),
																				1
																			),
																		]),
																	]),
																]),
																e("div", je, [
																	e(
																		"button",
																		{
																			onClick: k,
																			class: "absolute top-4 right-4 p-2 hover:bg-gray-100 dark:hover:bg-white/10 rounded-full transition",
																		},
																		Ae
																	),
																	Me,
																	De,
																	e("div", ze, [
																		(o(),
																		s(
																			S,
																			null,
																			z(x, (g) =>
																				e(
																					"button",
																					{
																						key: g.mode,
																						onClick: (
																							R
																						) =>
																							m(
																								g.mode
																							),
																						class: f([
																							"w-full flex items-center justify-between p-3 border rounded-xl transition-all",
																							w(
																								g.mode
																							)
																								? "border-[#D4AF37] bg-[#D4AF37]/10 ring-1 ring-[#D4AF37]"
																								: "border-gray-200 hover:border-gray-400 dark:border-white/10 dark:hover:border-white/30",
																						]),
																					},
																					[
																						e(
																							"div",
																							Ie,
																							[
																								e(
																									"div",
																									{
																										class: f(
																											[
																												"w-8 h-8 rounded-full flex items-center justify-center",
																												g.type ===
																												"Cash"
																													? "bg-green-100 text-green-600"
																													: "bg-blue-100 text-blue-600",
																											]
																										),
																									},
																									[
																										g.type ===
																										"Cash"
																											? (o(),
																											  s(
																													"svg",
																													Ve,
																													Pe
																											  ))
																											: (o(),
																											  s(
																													"svg",
																													Te,
																													He
																											  )),
																									],
																									2
																								),
																								e(
																									"span",
																									Le,
																									n(
																										g.mode
																									),
																									1
																								),
																							]
																						),
																						w(g.mode)
																							? (o(),
																							  s(
																									"div",
																									Ee
																							  ))
																							: j(
																									"",
																									!0
																							  ),
																					],
																					10,
																					Be
																				)
																			),
																			64
																		)),
																	]),
																	a.value.length > 1
																		? (o(),
																		  s("div", Ge, [
																				Ke,
																				(o(!0),
																				s(
																					S,
																					null,
																					z(
																						a.value,
																						(g) => (
																							o(),
																							s(
																								"div",
																								{
																									key: g.mode,
																									class: "flex items-center justify-between mb-2",
																								},
																								[
																									e(
																										"span",
																										Ue,
																										n(
																											g.mode
																										),
																										1
																									),
																									e(
																										"div",
																										We,
																										[
																											Ne,
																											H(
																												e(
																													"input",
																													{
																														type: "number",
																														"onUpdate:modelValue":
																															(
																																R
																															) =>
																																(g.amount =
																																	R),
																														onInput:
																															(
																																R
																															) =>
																																p(
																																	g.mode
																																),
																														class: "w-24 px-2 py-1 bg-white dark:bg-[#0F1115] border border-gray-200 dark:border-white/10 rounded text-right font-mono text-sm",
																														min: "0",
																														max: t(
																															d
																														),
																													},
																													null,
																													40,
																													qe
																												),
																												[
																													[
																														W,
																														g.amount,
																														void 0,
																														{
																															number: !0,
																														},
																													],
																												]
																											),
																										]
																									),
																								]
																							)
																						)
																					),
																					128
																				)),
																				e("div", Ye, [
																					Ze,
																					e(
																						"span",
																						{
																							class: f(
																								t(
																									$
																								) ===
																									0
																									? "text-green-500 font-bold"
																									: "text-red-500 font-bold"
																							),
																						},
																						n(M(t($))),
																						3
																					),
																				]),
																		  ]))
																		: j("", !0),
																	e("div", Qe, [
																		e(
																			"button",
																			{
																				onClick: V,
																				disabled:
																					!t(F) ||
																					h.value,
																				class: f([
																					"w-full py-4 rounded-xl font-bold text-lg shadow-xl transition-all flex items-center justify-center gap-2 transform active:scale-95",
																					!t(F) ||
																					h.value
																						? "bg-gray-100 text-gray-400 cursor-not-allowed dark:bg-white/5 dark:text-gray-600"
																						: "bg-gray-900 text-white hover:bg-black dark:bg-[#D4AF37] dark:text-black dark:hover:bg-[#b5952f]",
																				]),
																			},
																			[
																				h.value
																					? (o(),
																					  s(
																							"span",
																							Xe
																					  ))
																					: t(F)
																					? (o(),
																					  s(
																							"span",
																							tt,
																							"Confirm " +
																								n(
																									M(
																										t(
																											d
																										)
																									)
																								),
																							1
																					  ))
																					: (o(),
																					  s(
																							"span",
																							et,
																							n(
																								a
																									.value
																									.length ===
																									0
																									? "Select Payment"
																									: "Enter Amounts"
																							),
																							1
																					  )),
																			],
																			10,
																			Je
																		),
																	]),
																]),
															],
															64
													  ))
													: u.value === "success"
													? (o(),
													  s("div", ot, [
															st,
															rt,
															at,
															e("div", nt, [
																e("div", lt, [
																	it,
																	e(
																		"span",
																		dt,
																		n(
																			b.value ||
																				"POS-2025-001"
																		),
																		1
																	),
																]),
																e("div", ct, [
																	ut,
																	e("span", ht, n(M(t(d))), 1),
																]),
																l.value
																	? (o(), s("div", xt, bt))
																	: j("", !0),
															]),
															e(
																"div",
																{ class: "flex gap-3 w-full" },
																[
																	e(
																		"button",
																		{
																			onClick: k,
																			class: "flex-1 py-3 rounded-lg font-bold text-gray-700 bg-gray-100 hover:bg-gray-200 dark:bg-white/5 dark:text-gray-300 dark:hover:bg-white/10 transition",
																		},
																		" New Order "
																	),
																	ft,
																]
															),
													  ]))
													: j("", !0),
											],
											2
										),
								  ]))
								: j("", !0),
						]),
						_: 1,
					}
				)
			);
		},
	};
var _t = K(vt, [["__scopeId", "data-v-7900f27f"]]);
const yt = {
		class: "p-4 border-b border-gray-100 dark:border-white/5 flex items-center justify-between bg-gray-50 dark:bg-[#15171e]",
	},
	mt = { class: "text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2" },
	kt = e("span", null, "\u{1F6D2}", -1),
	wt = O(" Shopping Bag "),
	$t = { class: "text-xs font-normal text-gray-500 dark:text-gray-400" },
	Ft = { class: "flex items-center gap-2" },
	Ct = e(
		"svg",
		{ class: "w-5 h-5", fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
		[
			e("path", {
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M6 18L18 6M6 6l12 12",
			}),
		],
		-1
	),
	jt = [Ct],
	St = {
		key: 0,
		class: "flex-1 flex flex-col items-center justify-center text-gray-400 dark:text-gray-600",
	},
	At = e(
		"svg",
		{
			class: "w-16 h-16 mb-4 text-gray-200 dark:text-gray-700",
			fill: "none",
			stroke: "currentColor",
			viewBox: "0 0 24 24",
		},
		[
			e("path", {
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z",
			}),
		],
		-1
	),
	Mt = e("p", null, "Your bag is empty.", -1),
	Dt = { key: 1, class: "flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar" },
	zt = {
		class: "w-16 h-16 bg-gray-100 dark:bg-[#0F1115] rounded-lg flex-shrink-0 overflow-hidden border border-gray-200 dark:border-white/5 relative",
	},
	Bt = ["src"],
	It = {
		key: 1,
		class: "w-full h-full flex items-center justify-center text-xs text-gray-400 dark:text-gray-600",
	},
	Vt = {
		key: 2,
		class: "absolute bottom-0 right-0 bg-black dark:bg-[#D4AF37] text-white dark:text-black text-[10px] font-bold px-1.5 py-0.5 rounded-tl-md",
	},
	Ot = { class: "flex-1 min-w-0" },
	Pt = { class: "text-sm font-bold text-gray-900 dark:text-white truncate" },
	Tt = { class: "text-xs text-gray-500 dark:text-gray-400 truncate" },
	Rt = { class: "flex items-center gap-2 mt-1" },
	Ht = {
		class: "text-[10px] uppercase font-bold bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-500 px-1.5 py-0.5 rounded",
	},
	Lt = {
		class: "text-[10px] uppercase font-bold bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-300 px-1.5 py-0.5 rounded",
	},
	Et = { class: "mt-2 flex items-center justify-between" },
	Gt = { class: "flex flex-col" },
	Kt = { class: "text-xs text-gray-400 dark:text-gray-500" },
	Ut = { class: "font-mono text-sm font-bold text-gray-900 dark:text-white" },
	Wt = ["onClick"],
	Nt = e(
		"svg",
		{ class: "w-4 h-4", fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
		[
			e("path", {
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16",
			}),
		],
		-1
	),
	qt = [Nt],
	Yt = {
		key: 2,
		class: "p-6 bg-gray-50 dark:bg-[#15171e] border-t border-gray-200 dark:border-white/5",
	},
	Zt = { class: "space-y-2 mb-4 text-sm" },
	Qt = { class: "flex justify-between text-gray-600 dark:text-gray-400" },
	Jt = e("span", null, "Subtotal", -1),
	Xt = { class: "flex justify-between text-gray-600 dark:text-gray-400" },
	eo = {
		class: "flex justify-between text-lg font-bold text-gray-900 dark:text-white pt-2 border-t border-gray-200 dark:border-white/10",
	},
	to = e("span", null, "Total", -1),
	oo = {
		props: ["isOpen"],
		emits: ["close"],
		setup(v, { emit: r }) {
			const i = L(),
				c = C(!1);
			function h() {
				r("close");
			}
			function u(b) {
				return b
					? new Intl.NumberFormat("en-US", {
							style: "currency",
							currency: "USD",
					  }).format(b)
					: "$0.00";
			}
			return (b, l) => (
				o(),
				s("div", null, [
					v.isOpen
						? (o(),
						  s("div", {
								key: 0,
								onClick: h,
								class: "fixed inset-0 bg-gray-900/50 backdrop-blur-sm z-40 transition-opacity",
						  }))
						: j("", !0),
					e(
						"div",
						{
							class: f([
								"fixed top-0 right-0 h-full w-full sm:w-[400px] bg-white dark:bg-[#1a1c23] shadow-2xl z-50 transform transition-transform duration-300 ease-in-out flex flex-col border-l border-transparent dark:border-white/5",
								v.isOpen ? "translate-x-0" : "translate-x-full",
							]),
						},
						[
							e("div", yt, [
								e("h2", mt, [
									kt,
									wt,
									e("span", $t, "(" + n(t(i).totalItems) + " items)", 1),
								]),
								e("div", Ft, [
									t(i).items.length > 0
										? (o(),
										  s(
												"button",
												{
													key: 0,
													onClick:
														l[0] || (l[0] = (a) => t(i).clearCart()),
													class: "text-xs font-bold text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 px-2 py-1 rounded transition-colors",
												},
												" Clear "
										  ))
										: j("", !0),
									e(
										"button",
										{
											onClick: h,
											class: "p-2 hover:bg-gray-200 dark:hover:bg-white/10 rounded-full transition-colors text-gray-500 dark:text-gray-400",
										},
										jt
									),
								]),
							]),
							t(i).items.length === 0
								? (o(),
								  s("div", St, [
										At,
										Mt,
										e(
											"button",
											{
												onClick: h,
												class: "mt-4 text-sm text-[#D4AF37] font-medium hover:underline",
											},
											"Start Browsing"
										),
								  ]))
								: (o(),
								  s("div", Dt, [
										(o(!0),
										s(
											S,
											null,
											z(
												t(i).items,
												(a, x) => (
													o(),
													s(
														"div",
														{
															key: x,
															class: "flex gap-4 border-b border-gray-100 dark:border-white/5 pb-4 last:border-0",
														},
														[
															e("div", zt, [
																a.image
																	? (o(),
																	  s(
																			"img",
																			{
																				key: 0,
																				src: a.image,
																				loading: "lazy",
																				class: "w-full h-full object-cover",
																			},
																			null,
																			8,
																			Bt
																	  ))
																	: (o(),
																	  s("div", It, "No Img")),
																a.qty > 1
																	? (o(),
																	  s(
																			"div",
																			Vt,
																			" x" + n(a.qty),
																			1
																	  ))
																	: j("", !0),
															]),
															e("div", Ot, [
																e("h3", Pt, n(a.item_name), 1),
																e("p", Tt, n(a.item_code), 1),
																e("div", Rt, [
																	e("span", Ht, n(a.metal), 1),
																	e("span", Lt, n(a.purity), 1),
																]),
																e("div", Et, [
																	e("div", Gt, [
																		e(
																			"span",
																			Kt,
																			n(u(a.amount)) + " ea",
																			1
																		),
																		e(
																			"span",
																			Ut,
																			n(u(a.amount * a.qty)),
																			1
																		),
																	]),
																	e(
																		"button",
																		{
																			onClick: (d) =>
																				t(i).removeItem(x),
																			class: "text-red-400 hover:text-red-600 p-1 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors",
																			title: "Remove Item",
																		},
																		qt,
																		8,
																		Wt
																	),
																]),
															]),
														]
													)
												)
											),
											128
										)),
								  ])),
							t(i).items.length > 0
								? (o(),
								  s("div", Yt, [
										e("div", Zt, [
											e("div", Qt, [
												Jt,
												e("span", null, n(u(t(i).subtotal)), 1),
											]),
											e("div", Xt, [
												e(
													"span",
													null,
													"Tax (" + n(t(i).taxRate) + "%)",
													1
												),
												e("span", null, n(u(t(i).tax)), 1),
											]),
											e("div", eo, [
												to,
												e("span", null, n(u(t(i).grandTotal)), 1),
											]),
										]),
										e(
											"button",
											{
												onClick: l[1] || (l[1] = (a) => (c.value = !0)),
												class: "w-full bg-gray-900 dark:bg-[#D4AF37] text-white dark:text-black py-3 rounded-lg font-bold shadow-lg hover:bg-gray-800 dark:hover:bg-[#b5952f] active:scale-95 transition-all",
											},
											" Checkout "
										),
								  ]))
								: j("", !0),
						],
						2
					),
					I(
						_t,
						{ show: c.value, onClose: l[2] || (l[2] = (a) => (c.value = !1)) },
						null,
						8,
						["show"]
					),
				])
			);
		},
	},
	so = { class: "select-none px-2 py-4" },
	ro = { class: "flex items-center justify-between mb-6 px-1" },
	ao = e(
		"h3",
		{ class: "text-[10px] font-bold text-[#555961] uppercase tracking-widest" },
		"Filters",
		-1
	),
	no = { class: "mb-6 pb-5 border-b border-white/5" },
	lo = e(
		"label",
		{ class: "block text-[10px] font-bold text-gray-500 mb-3 px-1" },
		"Stock Status",
		-1
	),
	io = { class: "flex flex-col gap-2" },
	co = e(
		"svg",
		{
			class: "w-4 h-4 flex-shrink-0",
			fill: "none",
			stroke: "currentColor",
			viewBox: "0 0 24 24",
		},
		[
			e("path", {
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z",
			}),
		],
		-1
	),
	uo = O(" All Items "),
	ho = [co, uo],
	xo = e(
		"svg",
		{
			class: "w-4 h-4 flex-shrink-0",
			fill: "none",
			stroke: "currentColor",
			viewBox: "0 0 24 24",
		},
		[
			e("path", {
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
			}),
		],
		-1
	),
	go = O(" In Stock Only "),
	po = [xo, go],
	bo = e(
		"svg",
		{
			class: "w-4 h-4 flex-shrink-0",
			fill: "none",
			stroke: "currentColor",
			viewBox: "0 0 24 24",
		},
		[
			e("path", {
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
			}),
		],
		-1
	),
	fo = O(" Out of Stock "),
	vo = [bo, fo],
	_o = { class: "mb-6" },
	yo = e("label", { class: "block text-[10px] font-bold text-gray-500 mb-3 px-1" }, "Metal", -1),
	mo = { class: "flex flex-wrap gap-2" },
	ko = ["onClick"],
	wo = { class: "mb-6" },
	$o = e(
		"label",
		{ class: "block text-[10px] font-bold text-gray-500 mb-3 px-1" },
		"Gemstone",
		-1
	),
	Fo = { class: "flex flex-wrap gap-2" },
	Co = ["onClick"],
	jo = { class: "mb-6" },
	So = e(
		"label",
		{ class: "block text-[10px] font-bold text-gray-500 mb-2 px-1" },
		"Purity",
		-1
	),
	Ao = { class: "relative" },
	Mo = ["value"],
	Do = { value: "" },
	zo = ["value"],
	Bo = { key: 0, class: "mt-6 p-4 bg-amber-500/10 border border-amber-500/20 rounded-lg" },
	Io = { class: "flex items-start gap-3" },
	Vo = e(
		"svg",
		{
			class: "w-5 h-5 text-amber-500 flex-shrink-0 mt-0.5",
			fill: "none",
			stroke: "currentColor",
			viewBox: "0 0 24 24",
		},
		[
			e("path", {
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z",
			}),
		],
		-1
	),
	Oo = e("p", { class: "text-amber-500 font-bold text-xs mb-1" }, "Low Stock Alert", -1),
	Po = { class: "text-gray-400 text-[10px] leading-relaxed" },
	To = {
		setup(v) {
			const r = Z(),
				i = ["Diamond", "Ruby", "Sapphire", "Emerald", "Polki", "Kundan", "No Stone"],
				c = {
					"Yellow Gold": ["24K", "22K", "18K", "14K"],
					"White Gold": ["18K", "14K"],
					"Rose Gold": ["18K", "14K"],
					Platinum: ["950"],
					Silver: ["925 Sterling", "999 Fine"],
				},
				h = C("all"),
				u = C(0),
				b = B(() => r.activeFilters.custom_metal_type || ""),
				l = B(() => r.activeFilters.custom_gemstone || ""),
				a = B(
					() =>
						Object.keys(r.activeFilters).length > 0 ||
						r.searchQuery ||
						h.value !== "all"
				),
				x = B(() =>
					b.value && c[b.value] ? c[b.value] : [...new Set(Object.values(c).flat())]
				);
			function d(w) {
				(h.value = w),
					w === "in-stock"
						? (r.setFilter("in_stock_only", !0), r.setFilter("out_of_stock_only", !1))
						: w === "out-of-stock"
						? (r.setFilter("out_of_stock_only", !0), r.setFilter("in_stock_only", !1))
						: (r.setFilter("in_stock_only", !1), r.setFilter("out_of_stock_only", !1));
			}
			function $(w) {
				r.activeFilters.custom_purity && r.setFilter("custom_purity", ""),
					r.setFilter("custom_metal_type", w);
			}
			function F(w) {
				r.setFilter("custom_gemstone", w);
			}
			return (w, m) => (
				o(),
				s("div", so, [
					e("div", ro, [
						ao,
						t(a)
							? (o(),
							  s(
									"button",
									{
										key: 0,
										onClick: m[0] || (m[0] = (p) => t(r).resetFilters()),
										class: "text-[10px] text-[#D4AF37] hover:text-yellow-300 transition-colors",
									},
									" Reset All "
							  ))
							: j("", !0),
					]),
					e("div", no, [
						lo,
						e("div", io, [
							e(
								"button",
								{
									onClick: m[1] || (m[1] = (p) => d("all")),
									class: f([
										h.value === "all"
											? "bg-[#D4AF37] text-[#0F1115] font-bold border-[#D4AF37]"
											: "bg-[#1C1F26] text-gray-400 border-white/5 hover:border-gray-600 hover:text-white",
										"w-full px-3 py-2.5 text-[11px] rounded-lg border transition-all text-left shadow-sm flex items-center gap-2",
									]),
								},
								ho,
								2
							),
							e(
								"button",
								{
									onClick: m[2] || (m[2] = (p) => d("in-stock")),
									class: f([
										h.value === "in-stock"
											? "bg-emerald-600 text-white font-bold border-emerald-600"
											: "bg-[#1C1F26] text-gray-400 border-white/5 hover:border-emerald-600 hover:text-emerald-400",
										"w-full px-3 py-2.5 text-[11px] rounded-lg border transition-all text-left shadow-sm flex items-center gap-2",
									]),
								},
								po,
								2
							),
							e(
								"button",
								{
									onClick: m[3] || (m[3] = (p) => d("out-of-stock")),
									class: f([
										h.value === "out-of-stock"
											? "bg-red-600 text-white font-bold border-red-600"
											: "bg-[#1C1F26] text-gray-400 border-white/5 hover:border-red-600 hover:text-red-400",
										"w-full px-3 py-2.5 text-[11px] rounded-lg border transition-all text-left shadow-sm flex items-center gap-2",
									]),
								},
								vo,
								2
							),
						]),
					]),
					e("div", _o, [
						yo,
						e("div", mo, [
							e(
								"button",
								{
									onClick: m[4] || (m[4] = (p) => $("")),
									class: f([
										t(b)
											? "bg-[#1C1F26] text-gray-400 border-white/5 hover:border-gray-600 hover:text-white"
											: "bg-[#D4AF37] text-[#0F1115] font-bold border-[#D4AF37]",
										"flex-1 min-w-[45%] px-3 py-2.5 text-[11px] rounded-lg border transition-all text-center shadow-sm",
									]),
								},
								" All ",
								2
							),
							(o(!0),
							s(
								S,
								null,
								z(
									Object.keys(c),
									(p) => (
										o(),
										s(
											"button",
											{
												key: p,
												onClick: (V) => $(p),
												class: f([
													t(b) === p
														? "bg-[#D4AF37] text-[#0F1115] font-bold border-[#D4AF37]"
														: "bg-[#1C1F26] text-gray-400 border-white/5 hover:border-gray-600 hover:text-white",
													"flex-1 min-w-[45%] px-3 py-2.5 text-[11px] rounded-lg border transition-all text-center shadow-sm",
												]),
											},
											n(p),
											11,
											ko
										)
									)
								),
								128
							)),
						]),
					]),
					e("div", wo, [
						$o,
						e("div", Fo, [
							e(
								"button",
								{
									onClick: m[5] || (m[5] = (p) => F("")),
									class: f([
										t(l)
											? "bg-[#1C1F26] text-gray-400 border-white/5 hover:border-gray-600 hover:text-white"
											: "bg-[#D4AF37] text-[#0F1115] font-bold border-[#D4AF37]",
										"flex-1 min-w-[45%] px-3 py-2.5 text-[11px] rounded-lg border transition-all text-center shadow-sm",
									]),
								},
								" Any ",
								2
							),
							(o(),
							s(
								S,
								null,
								z(i, (p) =>
									e(
										"button",
										{
											key: p,
											onClick: (V) => F(p),
											class: f([
												t(l) === p
													? "bg-[#D4AF37] text-[#0F1115] font-bold border-[#D4AF37]"
													: "bg-[#1C1F26] text-gray-400 border-white/5 hover:border-gray-600 hover:text-white",
												"flex-1 min-w-[45%] px-3 py-2.5 text-[11px] rounded-lg border transition-all text-center shadow-sm",
											]),
										},
										n(p),
										11,
										Co
									)
								),
								64
							)),
						]),
					]),
					e("div", jo, [
						So,
						e("div", Ao, [
							e(
								"select",
								{
									value: t(r).activeFilters.custom_purity || "",
									onChange:
										m[6] ||
										(m[6] = (p) =>
											t(r).setFilter("custom_purity", p.target.value)),
									class: "w-full bg-[#1C1F26] text-gray-300 text-xs border border-white/10 rounded-lg p-3 focus:border-[#D4AF37] focus:ring-1 focus:ring-[#D4AF37] outline-none cursor-pointer",
								},
								[
									e(
										"option",
										Do,
										n(t(b) ? `Any ${t(b)} Purity` : "Any Purity"),
										1
									),
									(o(!0),
									s(
										S,
										null,
										z(
											t(x),
											(p) => (
												o(), s("option", { key: p, value: p }, n(p), 9, zo)
											)
										),
										128
									)),
								],
								40,
								Mo
							),
						]),
					]),
					u.value > 0
						? (o(),
						  s("div", Bo, [
								e("div", Io, [
									Vo,
									e("div", null, [
										Oo,
										e(
											"p",
											Po,
											n(u.value) +
												" item" +
												n(u.value > 1 ? "s" : "") +
												" need" +
												n(u.value === 1 ? "s" : "") +
												" restocking",
											1
										),
									]),
								]),
						  ]))
						: j("", !0),
				])
			);
		},
	};
const A = (v) => (N("data-v-339ab303"), (v = v()), q(), v),
	Ro = {
		class: "flex h-screen w-screen bg-[#F8F9FA] dark:bg-[#050505] font-sans overflow-hidden transition-colors duration-300",
	},
	Ho = {
		class: "w-16 sm:w-20 lg:w-72 bg-[#1a1c23] dark:bg-black border-r border-white/5 flex flex-col shadow-2xl z-30 relative transition-all duration-300",
	},
	Lo = Y(
		'<div class="h-24 flex items-center justify-center lg:justify-start lg:px-8 border-b border-white/5" data-v-339ab303><div class="flex items-center gap-4 group cursor-default" data-v-339ab303><div class="w-12 h-12 bg-gradient-to-tr from-[#D4AF37] to-[#F2E6A0] rounded-lg flex items-center justify-center text-[#0F1115] font-serif font-black text-2xl shadow-[0_0_15px_rgba(212,175,55,0.3)] transform group-hover:scale-105 transition-transform duration-500" data-v-339ab303> Z </div><div class="hidden lg:flex flex-col justify-center" data-v-339ab303><h1 class="text-white font-serif font-bold text-2xl leading-none tracking-wide" data-v-339ab303>ZEVAR</h1><div class="flex justify-between w-full mt-1 px-0.5" data-v-339ab303><span class="text-[9px] text-gray-400 uppercase font-medium tracking-[0.38em]" data-v-339ab303>Jewelers</span></div></div></div></div>',
		1
	),
	Eo = { class: "flex-1 flex flex-col overflow-hidden" },
	Go = { class: "p-4 space-y-2 flex-1 overflow-y-auto custom-scrollbar" },
	Ko = A(() =>
		e(
			"div",
			{ class: "relative z-10 flex items-center gap-4" },
			[
				e(
					"svg",
					{
						class: "w-5 h-5 transition-colors",
						fill: "none",
						stroke: "currentColor",
						viewBox: "0 0 24 24",
					},
					[
						e("path", {
							"stroke-linecap": "round",
							"stroke-linejoin": "round",
							"stroke-width": "2",
							d: "M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z",
						}),
					]
				),
				e(
					"span",
					{ class: "hidden lg:block font-medium tracking-wide text-sm" },
					"POS Terminal"
				),
			],
			-1
		)
	),
	Uo = A(() =>
		e(
			"div",
			{ class: "relative z-10 flex items-center gap-4" },
			[
				e(
					"svg",
					{
						class: "w-5 h-5 transition-colors",
						fill: "none",
						stroke: "currentColor",
						viewBox: "0 0 24 24",
					},
					[
						e("path", {
							"stroke-linecap": "round",
							"stroke-linejoin": "round",
							"stroke-width": "2",
							d: "M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
						}),
					]
				),
				e(
					"span",
					{ class: "hidden lg:block font-medium tracking-wide text-sm" },
					"Sales History"
				),
			],
			-1
		)
	),
	Wo = A(() =>
		e(
			"div",
			{ class: "relative z-10 flex items-center gap-4" },
			[
				e(
					"svg",
					{
						class: "w-5 h-5 transition-colors",
						fill: "none",
						stroke: "currentColor",
						viewBox: "0 0 24 24",
					},
					[
						e("path", {
							"stroke-linecap": "round",
							"stroke-linejoin": "round",
							"stroke-width": "2",
							d: "M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10",
						}),
					]
				),
				e(
					"span",
					{ class: "hidden lg:block font-medium tracking-wide text-sm" },
					"Catalogues"
				),
			],
			-1
		)
	),
	No = A(() =>
		e(
			"div",
			{ class: "relative z-10 flex items-center gap-4" },
			[
				e(
					"svg",
					{
						class: "w-5 h-5",
						fill: "none",
						stroke: "currentColor",
						viewBox: "0 0 24 24",
					},
					[
						e("path", {
							"stroke-linecap": "round",
							"stroke-linejoin": "round",
							"stroke-width": "2",
							d: "M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z",
						}),
						e("path", {
							"stroke-linecap": "round",
							"stroke-linejoin": "round",
							"stroke-width": "2",
							d: "M15 12a3 3 0 11-6 0 3 3 0 016 0z",
						}),
					]
				),
				e(
					"span",
					{ class: "hidden lg:block font-medium tracking-wide text-sm" },
					"Repairs"
				),
			],
			-1
		)
	),
	qo = { key: 0, class: "mt-6 pt-6 border-t border-white/5 lg:block hidden" },
	Yo = { class: "p-4 border-t border-white/5 bg-[#1a1c23] dark:bg-black z-20" },
	Zo = { class: "flex items-center justify-between gap-2 group" },
	Qo = { class: "flex items-center gap-3 overflow-hidden" },
	Jo = {
		class: "w-8 h-8 rounded-full bg-gradient-to-br from-[#D4AF37] to-[#F2E6A0] flex items-center justify-center text-[#0F1115] font-bold text-xs shadow-inner",
	},
	Xo = { class: "hidden lg:flex flex-col min-w-0" },
	es = { class: "text-xs font-bold text-white truncate" },
	ts = { class: "text-[10px] text-gray-400 truncate" },
	os = { key: 0, class: "w-4 h-4", fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
	ss = A(() =>
		e(
			"path",
			{
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z",
			},
			null,
			-1
		)
	),
	rs = [ss],
	as = { key: 1, class: "w-4 h-4", fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
	ns = A(() =>
		e(
			"path",
			{
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z",
			},
			null,
			-1
		)
	),
	ls = [ns],
	is = { class: "flex-1 flex flex-col relative min-w-0" },
	ds = {
		class: "h-16 sm:h-20 bg-white dark:bg-[#0F1115] border-b border-gray-200 dark:border-gray-800 flex items-center justify-between px-3 sm:px-6 z-20 sticky top-0 shadow-sm transition-colors duration-300",
	},
	cs = { class: "flex items-center gap-4 flex-1 max-w-3xl" },
	us = { class: "relative group" },
	hs = A(() => e("option", { value: "null", disabled: "" }, "Select Store Location", -1)),
	xs = ["value"],
	gs = { class: "relative flex-1" },
	ps = A(() =>
		e(
			"svg",
			{
				class: "absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400",
				fill: "none",
				stroke: "currentColor",
				viewBox: "0 0 24 24",
			},
			[
				e("path", {
					"stroke-linecap": "round",
					"stroke-linejoin": "round",
					"stroke-width": "2",
					d: "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z",
				}),
			],
			-1
		)
	),
	bs = { class: "flex items-center gap-6" },
	fs = {
		class: "hidden lg:flex items-center gap-0 bg-gray-100 dark:bg-black text-gray-900 dark:text-white pl-4 pr-2 py-2 rounded-xl border border-gray-200 dark:border-gray-800 flex-1 max-w-2xl overflow-hidden transition-colors duration-300",
	},
	vs = Y(
		'<div class="flex items-center gap-2 border-r border-gray-300 dark:border-gray-800 pr-3 mr-3 flex-shrink-0" data-v-339ab303><span class="relative flex h-2 w-2" data-v-339ab303><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-500 opacity-75" data-v-339ab303></span><span class="relative inline-flex rounded-full h-2 w-2 bg-green-600" data-v-339ab303></span></span><span class="text-[10px] font-bold uppercase tracking-widest text-gray-500 dark:text-gray-400" data-v-339ab303>Live Spot</span></div>',
		1
	),
	_s = {
		class: "flex items-center gap-8 overflow-x-auto pr-2 custom-scrollbar-horizontal pb-2 pt-1",
	},
	ys = {
		class: "text-[11px] text-gray-500 dark:text-gray-400 uppercase font-bold whitespace-nowrap mb-0.5",
	},
	ms = { class: "text-lg font-mono font-bold text-[#D4AF37] tracking-wide" },
	ks = A(() =>
		e(
			"span",
			{ class: "text-[9px] text-gray-500 dark:text-gray-500 ml-0.5 font-normal" },
			"/oz",
			-1
		)
	),
	ws = A(() =>
		e(
			"svg",
			{
				class: "w-6 h-6 text-gray-600 dark:text-gray-300 group-hover:text-black dark:group-hover:text-white transition-colors",
				fill: "none",
				stroke: "currentColor",
				viewBox: "0 0 24 24",
			},
			[
				e("path", {
					"stroke-linecap": "round",
					"stroke-linejoin": "round",
					"stroke-width": "1.5",
					d: "M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z",
				}),
			],
			-1
		)
	),
	$s = {
		key: 0,
		class: "absolute top-1 right-0.5 h-5 w-5 flex items-center justify-center bg-[#D4AF37] text-white text-[10px] font-bold rounded-full shadow-md transform group-hover:scale-110 transition-transform",
	},
	Fs = {
		class: "flex-1 overflow-y-auto overflow-x-hidden p-3 sm:p-4 lg:p-6 bg-[#F8F9FA] dark:bg-[#050505] transition-colors duration-300",
	},
	Cs = {
		setup(v) {
			const r = re(),
				i = ae(),
				c = L(),
				h = Z(),
				u = C(!1),
				b = 31.1035,
				l = B(() => {
					if (!i.rates) return [];
					const x = [
						"Yellow Gold-24K",
						"Yellow Gold-22K",
						"Yellow Gold-18K",
						"Silver-925 Sterling",
					];
					return Object.entries(i.rates)
						.filter(([d]) => !d.includes("Platinum"))
						.map(([d, $]) => [d, ($ * b).toFixed(2)])
						.sort((d, $) => {
							const F = x.indexOf(d[0]),
								w = x.indexOf($[0]);
							return F !== -1 && w !== -1
								? F - w
								: F !== -1
								? -1
								: w !== -1
								? 1
								: d[0].localeCompare($[0]);
						});
				}),
				a = T({
					url: "frappe.client.get_list",
					params: {
						doctype: "Warehouse",
						filters: { is_group: 0, parent_warehouse: ["like", "%Zevar US Stores%"] },
						fields: ["name"],
					},
					auto: !0,
				});
			return (
				ee(() => {
					i.startPolling(),
						r.currentWarehouse && c.loadTaxForWarehouse(r.currentWarehouse);
				}),
				U(
					() => r.currentWarehouse,
					(x) => {
						x && c.loadTaxForWarehouse(x);
					}
				),
				(x, d) => {
					var F, w, m, p, V;
					const $ = te("router-link");
					return (
						o(),
						s("div", Ro, [
							e("aside", Ho, [
								Lo,
								e("div", Eo, [
									e("nav", Go, [
										I(
											$,
											{
												to: "/",
												class: f([
													"flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300 group relative overflow-hidden",
													x.$route.path === "/"
														? ""
														: "text-gray-400 hover:text-white hover:bg-white/5",
												]),
												"active-class":
													"bg-white/10 text-white shadow-inner",
											},
											{
												default: P(() => [
													Ko,
													e(
														"div",
														{
															class: f([
																"absolute left-0 top-0 h-full w-1 bg-[#D4AF37] shadow-[0_0_10px_#D4AF37] transition-opacity duration-300",
																x.$route.path === "/"
																	? "opacity-100"
																	: "opacity-0 group-hover:opacity-100",
															]),
														},
														null,
														2
													),
												]),
												_: 1,
											},
											8,
											["class"]
										),
										I(
											$,
											{
												to: "/transactions",
												class: f([
													"flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300 group relative overflow-hidden",
													x.$route.path === "/transactions"
														? ""
														: "text-gray-400 hover:text-white hover:bg-white/5",
												]),
												"active-class":
													"bg-white/10 text-white shadow-inner",
											},
											{
												default: P(() => [
													Uo,
													e(
														"div",
														{
															class: f([
																"absolute left-0 top-0 h-full w-1 bg-[#D4AF37] shadow-[0_0_10px_#D4AF37] transition-opacity duration-300",
																x.$route.path === "/transactions"
																	? "opacity-100"
																	: "opacity-0 group-hover:opacity-100",
															]),
														},
														null,
														2
													),
												]),
												_: 1,
											},
											8,
											["class"]
										),
										I(
											$,
											{
												to: "/catalogues",
												target: "_blank",
												class: f([
													"flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300 group relative overflow-hidden",
													x.$route.path === "/catalogues"
														? ""
														: "text-gray-400 hover:text-white hover:bg-white/5",
												]),
												"active-class":
													"bg-white/10 text-white shadow-inner",
											},
											{
												default: P(() => [
													Wo,
													e(
														"div",
														{
															class: f([
																"absolute left-0 top-0 h-full w-1 bg-[#D4AF37] shadow-[0_0_10px_#D4AF37] transition-opacity duration-300",
																x.$route.path === "/catalogues"
																	? "opacity-100"
																	: "opacity-0 group-hover:opacity-100",
															]),
														},
														null,
														2
													),
												]),
												_: 1,
											},
											8,
											["class"]
										),
										I(
											$,
											{
												to: "/repairs",
												class: f([
													"flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-300 group relative overflow-hidden",
													x.$route.path === "/repairs"
														? ""
														: "text-gray-400 hover:text-white hover:bg-white/5",
												]),
												"active-class":
													"bg-white/10 text-white shadow-inner",
											},
											{
												default: P(() => [
													No,
													e(
														"div",
														{
															class: f([
																"absolute left-0 top-0 h-full w-1 bg-[#D4AF37] shadow-[0_0_10px_#D4AF37] transition-opacity duration-300",
																x.$route.path === "/repairs"
																	? "opacity-100"
																	: "opacity-0 group-hover:opacity-100",
															]),
														},
														null,
														2
													),
												]),
												_: 1,
											},
											8,
											["class"]
										),
										x.$route.path === "/"
											? (o(), s("div", qo, [I(To)]))
											: j("", !0),
									]),
								]),
								e("div", Yo, [
									e("div", Zo, [
										e("div", Qo, [
											e(
												"div",
												Jo,
												n(
													((m =
														(w =
															(F = t(r).user) == null
																? void 0
																: F.full_name) == null
															? void 0
															: w[0]) == null
														? void 0
														: m.toUpperCase()) || "U"
												),
												1
											),
											e("div", Xo, [
												e(
													"span",
													es,
													n(
														((p = t(r).user) == null
															? void 0
															: p.full_name) || "Guest"
													),
													1
												),
												e(
													"span",
													ts,
													n(
														((V = t(r).user) == null
															? void 0
															: V.email) || ""
													),
													1
												),
											]),
										]),
										e(
											"button",
											{
												onClick:
													d[0] || (d[0] = (k) => t(h).toggleTheme()),
												class: "hidden lg:flex w-8 h-8 items-center justify-center rounded-lg bg-white/5 hover:bg-white/10 text-gray-400 hover:text-[#D4AF37] transition-colors border border-white/5 focus:outline-none",
												title: "Toggle Theme",
											},
											[
												t(h).isDark
													? (o(), s("svg", os, rs))
													: (o(), s("svg", as, ls)),
											]
										),
									]),
								]),
							]),
							e("div", is, [
								e("header", ds, [
									e("div", cs, [
										e("div", us, [
											H(
												e(
													"select",
													{
														"onUpdate:modelValue":
															d[1] ||
															(d[1] = (k) =>
																(t(r).currentWarehouse = k)),
														onChange:
															d[2] ||
															(d[2] = (k) =>
																t(r).setWarehouse(k.target.value)),
														class: "h-11 bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 pl-4 pr-10 rounded-lg text-sm font-bold text-gray-800 dark:text-gray-200 focus:ring-2 focus:ring-[#D4AF37] focus:border-[#D4AF37] cursor-pointer min-w-[200px] transition-all hover:bg-gray-100 dark:hover:bg-gray-700 shadow-sm outline-none",
													},
													[
														hs,
														(o(!0),
														s(
															S,
															null,
															z(
																t(a).data,
																(k) => (
																	o(),
																	s(
																		"option",
																		{
																			key: k.name,
																			value: k.name,
																		},
																		n(k.name),
																		9,
																		xs
																	)
																)
															),
															128
														)),
													],
													544
												),
												[[oe, t(r).currentWarehouse]]
											),
										]),
										e("div", gs, [
											ps,
											H(
												e(
													"input",
													{
														type: "text",
														"onUpdate:modelValue":
															d[3] ||
															(d[3] = (k) => (t(h).searchQuery = k)),
														placeholder: "Search collection...",
														class: "h-11 w-full bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg text-gray-800 dark:text-gray-200 placeholder-gray-400 dark:placeholder-gray-600 focus:ring-2 focus:ring-[#D4AF37] focus:border-transparent text-sm font-medium pl-11 transition-all",
													},
													null,
													512
												),
												[[W, t(h).searchQuery]]
											),
										]),
									]),
									e("div", bs, [
										e("div", fs, [
											vs,
											e("div", _s, [
												(o(!0),
												s(
													S,
													null,
													z(
														t(l),
														([k, M]) => (
															o(),
															s(
																"div",
																{
																	key: k,
																	class: "flex flex-col leading-tight flex-shrink-0 px-3",
																},
																[
																	e(
																		"span",
																		ys,
																		n(k.replace(/-/g, " ")),
																		1
																	),
																	e("span", ms, [
																		O("$" + n(M), 1),
																		ks,
																	]),
																]
															)
														)
													),
													128
												)),
											]),
										]),
										e(
											"button",
											{
												onClick: d[4] || (d[4] = (k) => (u.value = !0)),
												class: "relative p-3 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors group",
											},
											[
												ws,
												t(c).totalItems > 0
													? (o(), s("span", $s, n(t(c).totalItems), 1))
													: j("", !0),
											]
										),
									]),
								]),
								e("main", Fs, [se(x.$slots, "default", {}, void 0, !0)]),
							]),
							I(
								oo,
								{
									isOpen: u.value,
									onClose: d[5] || (d[5] = (k) => (u.value = !1)),
								},
								null,
								8,
								["isOpen"]
							),
						])
					);
				}
			);
		},
	};
var Ms = K(Cs, [["__scopeId", "data-v-339ab303"]]);
export { Ms as A, re as u };
