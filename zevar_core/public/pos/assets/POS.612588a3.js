var U = Object.defineProperty,
	E = Object.defineProperties;
var Q = Object.getOwnPropertyDescriptors;
var C = Object.getOwnPropertySymbols;
var I = Object.prototype.hasOwnProperty,
	L = Object.prototype.propertyIsEnumerable;
var N = (t, d, n) =>
		d in t
			? U(t, d, { enumerable: !0, configurable: !0, writable: !0, value: n })
			: (t[d] = n),
	z = (t, d) => {
		for (var n in d || (d = {})) I.call(d, n) && N(t, n, d[n]);
		if (C) for (var n of C(d)) L.call(d, n) && N(t, n, d[n]);
		return t;
	},
	A = (t, d) => E(t, Q(d));
var B = (t, d) => {
	var n = {};
	for (var i in t) I.call(t, i) && d.indexOf(i) < 0 && (n[i] = t[i]);
	if (t != null && C) for (var i of C(t)) d.indexOf(i) < 0 && L.call(t, i) && (n[i] = t[i]);
	return n;
};
import { u as R, A as J } from "./AppLayout.b973350d.js";
import {
	o,
	k as r,
	l as e,
	t as a,
	n as h,
	w as K,
	q as j,
	_ as P,
	i as m,
	x as X,
	j as D,
	y as M,
	b as G,
	z as T,
	u as $,
	F,
	A as V,
	T as Y,
	B as W,
	C as q,
	D as O,
} from "./vendor.b4720657.js";
import { u as H, a as Z } from "./ui.3a424cc5.js";
const ee = {
		class: "bg-white dark:bg-[#15171e] rounded-lg border border-gray-200 dark:border-gray-800 shadow-sm hover:shadow-md transition-all cursor-pointer flex flex-col h-full group relative overflow-hidden",
	},
	te = { class: "aspect-square bg-gray-100 dark:bg-gray-800 relative" },
	se = ["src"],
	oe = {
		key: 1,
		class: "w-full h-full flex items-center justify-center text-gray-300 dark:text-gray-700",
	},
	re = e(
		"svg",
		{
			xmlns: "http://www.w3.org/2000/svg",
			class: "h-12 w-12",
			fill: "none",
			viewBox: "0 0 24 24",
			stroke: "currentColor",
		},
		[
			e("path", {
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "1",
				d: "M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z",
			}),
		],
		-1
	),
	ae = [re],
	ne = { class: "absolute top-2 right-2" },
	de = {
		key: 0,
		class: "bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-200 text-xs font-bold px-2 py-1 rounded-full",
	},
	ie = {
		key: 1,
		class: "bg-orange-100 text-orange-800 dark:bg-orange-900/50 dark:text-orange-200 text-xs font-bold px-2 py-1 rounded-full",
	},
	le = { class: "p-4 flex-1 flex flex-col" },
	ce = { class: "flex items-start justify-between mb-2" },
	ue = {
		class: "font-medium text-gray-900 dark:text-white line-clamp-2 text-sm leading-snug min-h-[2.5rem]",
	},
	he = { class: "flex flex-wrap gap-1 mb-3" },
	_e = {
		class: "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400",
	},
	ge = {
		class: "inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300",
	},
	xe = {
		key: 0,
		class: "text-[10px] text-gray-500 dark:text-gray-400 mb-3 space-y-0.5 bg-gray-50 dark:bg-white/5 p-2 rounded",
	},
	ye = { key: 0, class: "flex justify-between" },
	fe = e("span", null, "Gross:", -1),
	me = j(),
	be = { key: 1, class: "flex justify-between text-red-400 dark:text-red-400/80" },
	ve = e("span", null, "Stone:", -1),
	ke = j(),
	pe = {
		key: 2,
		class: "flex justify-between font-bold text-gray-700 dark:text-gray-300 border-t border-gray-200 dark:border-white/10 pt-0.5 mt-0.5",
	},
	we = e("span", null, "Net:", -1),
	$e = j(),
	Ce = {
		class: "mt-auto pt-3 border-t border-gray-50 dark:border-gray-800 flex items-center justify-between",
	},
	je = { class: "flex flex-col" },
	Se = e("span", { class: "text-xs text-gray-500 dark:text-gray-400" }, "Price", -1),
	Me = { class: "text-lg font-bold text-gray-900 dark:text-white" },
	Fe = ["onClick"],
	Ie = e(
		"svg",
		{
			xmlns: "http://www.w3.org/2000/svg",
			class: "h-5 w-5",
			fill: "none",
			viewBox: "0 0 24 24",
			stroke: "currentColor",
		},
		[
			e("path", {
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M12 4v16m8-8H4",
			}),
		],
		-1
	),
	Le = [Ie],
	Ne = {
		props: { item: { type: Object, required: !0, default: () => ({}) } },
		setup(t) {
			const d = t,
				n = H();
			function i() {
				n.addItem(d.item);
			}
			function s(c) {
				return c
					? new Intl.NumberFormat("en-US", {
							style: "currency",
							currency: "USD",
					  }).format(c)
					: "$0.00";
			}
			return (c, y) => (
				o(),
				r("div", ee, [
					e("div", te, [
						t.item.image
							? (o(),
							  r(
									"img",
									{
										key: 0,
										src: t.item.image,
										alt: "Item",
										class: "w-full h-full object-cover group-hover:scale-105 transition-transform duration-500",
										loading: "lazy",
									},
									null,
									8,
									se
							  ))
							: (o(), r("div", oe, ae)),
						e("div", ne, [
							t.item.stock_qty <= 0
								? (o(), r("span", de, " Out of Stock "))
								: t.item.stock_qty < 5
								? (o(),
								  r("span", ie, " Only " + a(t.item.stock_qty) + " left ", 1))
								: h("", !0),
						]),
					]),
					e("div", le, [
						e("div", ce, [e("h3", ue, a(t.item.item_name), 1)]),
						e("div", he, [
							e("span", _e, a(t.item.metal || "Gold"), 1),
							e("span", ge, a(t.item.purity || "Standard"), 1),
						]),
						t.item.net_weight > 0 || t.item.gross_weight > 0
							? (o(),
							  r("div", xe, [
									t.item.gross_weight > 0
										? (o(),
										  r("div", ye, [
												fe,
												me,
												e("span", null, a(t.item.gross_weight) + "g", 1),
										  ]))
										: h("", !0),
									t.item.stone_weight > 0
										? (o(),
										  r("div", be, [
												ve,
												ke,
												e(
													"span",
													null,
													"-" + a(t.item.stone_weight) + "g",
													1
												),
										  ]))
										: h("", !0),
									t.item.net_weight > 0
										? (o(),
										  r("div", pe, [
												we,
												$e,
												e("span", null, a(t.item.net_weight) + "g", 1),
										  ]))
										: h("", !0),
							  ]))
							: h("", !0),
						e("div", Ce, [
							e("div", je, [Se, e("span", Me, a(s(t.item.price)), 1)]),
							e(
								"button",
								{
									onClick: K(i, ["stop"]),
									class: "bg-gray-900 dark:bg-white text-white dark:text-black p-2 rounded-lg hover:bg-gray-700 dark:hover:bg-gray-200 transition-colors shadow-md active:scale-95",
									title: "Add to Cart",
								},
								Le,
								8,
								Fe
							),
						]),
					]),
				])
			);
		},
	};
const _ = (t) => (W("data-v-5e9c2fbc"), (t = t()), q(), t),
	ze = { key: 0, class: "fixed inset-0 z-[100] flex items-center justify-center p-4 sm:p-6" },
	Ae = {
		class: "relative bg-white dark:bg-[#1a1c23] rounded-xl shadow-2xl w-full max-w-4xl overflow-hidden flex flex-col md:flex-row max-h-[90vh] border border-transparent dark:border-white/10 transition-all",
	},
	Be = _(() =>
		e(
			"svg",
			{
				class: "h-6 w-6 text-gray-600 dark:text-white group-hover:scale-110 transition-transform",
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
	Pe = [Be],
	De = {
		class: "w-full md:w-1/2 bg-gray-50 dark:bg-[#0F1115] flex items-center justify-center p-8 border-r border-gray-100 dark:border-white/5 relative",
	},
	Ge = ["src"],
	Te = { key: 1, class: "text-gray-300 dark:text-gray-700" },
	Ve = _(() =>
		e(
			"svg",
			{ class: "h-32 w-32", fill: "none", viewBox: "0 0 24 24", stroke: "currentColor" },
			[
				e("path", {
					"stroke-linecap": "round",
					"stroke-linejoin": "round",
					"stroke-width": "1",
					d: "M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z",
				}),
			],
			-1
		)
	),
	We = [Ve],
	qe = { class: "w-full md:w-1/2 p-8 overflow-y-auto bg-white dark:bg-[#1a1c23]" },
	Oe = { key: 0, class: "h-full flex items-center justify-center" },
	He = _(() =>
		e(
			"div",
			{
				class: "animate-spin rounded-full h-8 w-8 border-2 border-gray-900 dark:border-[#D4AF37] border-t-transparent",
			},
			null,
			-1
		)
	),
	Ue = [He],
	Ee = { key: 1 },
	Qe = { class: "mb-6" },
	Re = { class: "text-2xl font-serif font-bold text-gray-900 dark:text-white leading-tight" },
	Je = { class: "text-sm text-gray-500 dark:text-gray-400 mt-1 font-mono tracking-wide" },
	Ke = { class: "flex gap-2 mb-8" },
	Xe = {
		key: 0,
		class: "px-3 py-1 bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-500 rounded text-xs font-bold uppercase tracking-wider border border-yellow-200 dark:border-yellow-700/50",
	},
	Ye = {
		key: 1,
		class: "px-3 py-1 bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300 rounded text-xs font-bold uppercase tracking-wider border border-gray-200 dark:border-gray-700",
	},
	Ze = {
		class: "bg-gray-50 dark:bg-[#15171e] rounded-xl p-5 mb-6 text-sm border border-gray-100 dark:border-white/5",
	},
	et = { class: "flex justify-between mb-2 text-gray-600 dark:text-gray-400" },
	tt = _(() => e("span", null, "Gross Weight", -1)),
	st = { class: "font-medium text-gray-900 dark:text-gray-200" },
	ot = { class: "flex justify-between mb-2 text-red-400 dark:text-red-400/80" },
	rt = _(() => e("span", null, "- Stone Weight", -1)),
	at = { class: "flex justify-between pt-3 border-t border-gray-200 dark:border-white/10 mt-1" },
	nt = _(() =>
		e("span", { class: "font-bold text-gray-700 dark:text-white" }, "Net Weight", -1)
	),
	dt = { class: "font-bold text-gray-900 dark:text-[#D4AF37] text-base" },
	it = { key: 0, class: "mb-6" },
	lt = _(() =>
		e(
			"h4",
			{
				class: "text-xs font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-3",
			},
			"Gemstone Details",
			-1
		)
	),
	ct = {
		class: "bg-white dark:bg-[#0F1115] rounded-lg border border-gray-100 dark:border-white/10 overflow-hidden",
	},
	ut = { class: "w-full text-sm text-left" },
	ht = _(() =>
		e(
			"thead",
			{ class: "bg-gray-50 dark:bg-white/5" },
			[
				e("tr", { class: "text-xs text-gray-500 dark:text-gray-400 uppercase" }, [
					e("th", { class: "px-4 py-2 font-medium" }, "Stone"),
					e("th", { class: "px-4 py-2 font-medium text-right" }, "Carat"),
				]),
			],
			-1
		)
	),
	_t = { class: "divide-y divide-gray-100 dark:divide-white/5" },
	gt = { class: "px-4 py-2.5" },
	xt = { class: "font-medium text-gray-900 dark:text-gray-200" },
	yt = { class: "text-[10px] text-gray-500 dark:text-gray-500" },
	ft = { class: "px-4 py-2.5 text-right font-mono text-gray-700 dark:text-gray-300" },
	mt = { class: "space-y-3 mb-8 pt-2" },
	bt = { class: "flex justify-between text-sm" },
	vt = _(() => e("span", { class: "text-gray-500 dark:text-gray-400" }, "Gold Rate (Live)", -1)),
	kt = { class: "text-gray-900 dark:text-gray-300 font-medium" },
	pt = { class: "flex justify-between text-sm" },
	wt = _(() => e("span", { class: "text-gray-500 dark:text-gray-400" }, "Gold Value", -1)),
	$t = { class: "text-gray-900 dark:text-gray-300 font-medium" },
	Ct = { key: 1, class: "flex justify-between text-sm" },
	jt = _(() =>
		e(
			"span",
			{ class: "text-purple-600 dark:text-purple-400 font-medium" },
			"Gemstone Value",
			-1
		)
	),
	St = { class: "text-purple-700 dark:text-purple-300 font-bold" },
	Mt = {
		class: "flex justify-between items-end pt-4 border-t border-gray-100 dark:border-white/10 mt-2",
	},
	Ft = _(() =>
		e("span", { class: "text-lg font-bold text-gray-900 dark:text-white" }, "Total Price", -1)
	),
	It = { key: 0, class: "ml-2 text-xs text-gray-400" },
	Lt = { class: "text-3xl font-serif font-bold text-gray-900 dark:text-white tracking-tight" },
	Nt = _(() =>
		e(
			"svg",
			{ class: "w-5 h-5", fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
			[
				e("path", {
					"stroke-linecap": "round",
					"stroke-linejoin": "round",
					"stroke-width": "2",
					d: "M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z",
				}),
			],
			-1
		)
	),
	zt = j(" Add to Cart "),
	At = [Nt, zt],
	Bt = {
		props: ["show", "itemCode"],
		emits: ["close"],
		setup(t, { emit: d }) {
			const n = t,
				i = H(),
				s = m({}),
				c = m(!1),
				y = X(() => {
					if (s.value.net_weight) return s.value.net_weight;
					const l = s.value.gross_weight || 0,
						u = s.value.stone_weight || 0;
					return Math.max(0, l - u);
				}),
				p = D({
					url: "zevar_core.api.pricing.get_item_price",
					makeParams() {
						return { item_code: n.itemCode };
					},
					onSuccess(l) {
						(s.value = A(z({}, l), { item_code: n.itemCode })), (c.value = !1);
					},
				});
			M(
				() => n.show,
				(l) => {
					l && n.itemCode && ((c.value = !0), (s.value = {}), p.fetch());
				}
			);
			function v() {
				!s.value.item_code || (i.addItem(s.value), d("close"));
			}
			function g() {
				d("close");
			}
			function k(l) {
				return l
					? new Intl.NumberFormat("en-US", {
							style: "currency",
							currency: "USD",
					  }).format(l)
					: "$0.00";
			}
			function w(l) {
				return !l && l !== 0 ? "0.000" : parseFloat(l).toFixed(3);
			}
			return (l, u) => (
				o(),
				G(
					Y,
					{ name: "fade" },
					{
						default: T(() => [
							t.show
								? (o(),
								  r("div", ze, [
										e("div", {
											onClick: g,
											class: "absolute inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity",
										}),
										e("div", Ae, [
											e(
												"button",
												{
													onClick: g,
													class: "absolute top-4 right-4 z-10 p-2 bg-white/80 dark:bg-black/50 backdrop-blur rounded-full hover:bg-gray-100 dark:hover:bg-white/20 transition-colors group",
												},
												Pe
											),
											e("div", De, [
												s.value.image
													? (o(),
													  r(
															"img",
															{
																key: 0,
																src: s.value.image,
																class: "max-h-[60vh] object-contain drop-shadow-xl transform hover:scale-105 transition-transform duration-500",
															},
															null,
															8,
															Ge
													  ))
													: (o(), r("div", Te, We)),
											]),
											e("div", qe, [
												c.value
													? (o(), r("div", Oe, Ue))
													: (o(),
													  r("div", Ee, [
															e("div", Qe, [
																e(
																	"h2",
																	Re,
																	a(s.value.item_name),
																	1
																),
																e(
																	"p",
																	Je,
																	a(s.value.item_code),
																	1
																),
															]),
															e("div", Ke, [
																s.value.metal
																	? (o(),
																	  r(
																			"span",
																			Xe,
																			a(s.value.metal),
																			1
																	  ))
																	: h("", !0),
																s.value.purity
																	? (o(),
																	  r(
																			"span",
																			Ye,
																			a(s.value.purity),
																			1
																	  ))
																	: h("", !0),
															]),
															e("div", Ze, [
																e("div", et, [
																	tt,
																	e(
																		"span",
																		st,
																		a(
																			w(s.value.gross_weight)
																		) + " g",
																		1
																	),
																]),
																e("div", ot, [
																	rt,
																	e(
																		"span",
																		null,
																		a(
																			w(s.value.stone_weight)
																		) + " g",
																		1
																	),
																]),
																e("div", at, [
																	nt,
																	e(
																		"span",
																		dt,
																		a(w($(y))) + " g",
																		1
																	),
																]),
															]),
															s.value.gemstones &&
															s.value.gemstones.length > 0
																? (o(),
																  r("div", it, [
																		lt,
																		e("div", ct, [
																			e("table", ut, [
																				ht,
																				e("tbody", _t, [
																					(o(!0),
																					r(
																						F,
																						null,
																						V(
																							s.value
																								.gemstones,
																							(
																								x,
																								f
																							) => (
																								o(),
																								r(
																									"tr",
																									{
																										key: f,
																									},
																									[
																										e(
																											"td",
																											gt,
																											[
																												e(
																													"div",
																													xt,
																													a(
																														x.gem_type
																													),
																													1
																												),
																												e(
																													"div",
																													yt,
																													a(
																														x.cut
																													) +
																														" \u2022 " +
																														a(
																															x.color
																														) +
																														" \u2022 " +
																														a(
																															x.clarity
																														),
																													1
																												),
																											]
																										),
																										e(
																											"td",
																											ft,
																											a(
																												x.carat
																											),
																											1
																										),
																									]
																								)
																							)
																						),
																						128
																					)),
																				]),
																			]),
																		]),
																  ]))
																: h("", !0),
															e("div", mt, [
																s.value.net_weight > 0 &&
																s.value.gold_rate > 0
																	? (o(),
																	  r(
																			F,
																			{ key: 0 },
																			[
																				e("div", bt, [
																					vt,
																					e(
																						"span",
																						kt,
																						a(
																							k(
																								s
																									.value
																									.gold_rate
																							)
																						) + " /g",
																						1
																					),
																				]),
																				e("div", pt, [
																					wt,
																					e(
																						"span",
																						$t,
																						a(
																							k(
																								s
																									.value
																									.gold_value
																							)
																						),
																						1
																					),
																				]),
																			],
																			64
																	  ))
																	: h("", !0),
																s.value.gemstone_value > 0
																	? (o(),
																	  r("div", Ct, [
																			jt,
																			e(
																				"span",
																				St,
																				a(
																					k(
																						s.value
																							.gemstone_value
																					)
																				),
																				1
																			),
																	  ]))
																	: h("", !0),
																e("div", Mt, [
																	e("div", null, [
																		Ft,
																		s.value.price_source
																			? (o(),
																			  r(
																					"span",
																					It,
																					"(" +
																						a(
																							s.value
																								.price_source
																						) +
																						")",
																					1
																			  ))
																			: h("", !0),
																	]),
																	e(
																		"span",
																		Lt,
																		a(k(s.value.final_price)),
																		1
																	),
																]),
															]),
															e(
																"button",
																{
																	onClick: v,
																	class: "w-full bg-gray-900 text-white dark:bg-[#D4AF37] dark:text-black py-4 rounded-xl font-bold text-lg hover:bg-gray-800 dark:hover:bg-[#b5952f] transition-all shadow-lg hover:shadow-xl transform active:scale-95 flex items-center justify-center gap-2",
																},
																At
															),
													  ])),
											]),
										]),
								  ]))
								: h("", !0),
						]),
						_: 1,
					}
				)
			);
		},
	};
var Pt = P(Bt, [["__scopeId", "data-v-5e9c2fbc"]]);
const b = (t) => (W("data-v-f6828a1e"), (t = t()), q(), t),
	Dt = {
		key: 0,
		class: "h-full flex flex-col items-center justify-center text-center opacity-50",
	},
	Gt = b(() =>
		e(
			"div",
			{ class: "w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mb-4" },
			[
				e(
					"svg",
					{
						class: "w-8 h-8 text-gray-400",
						fill: "none",
						stroke: "currentColor",
						viewBox: "0 0 24 24",
					},
					[
						e("path", {
							"stroke-linecap": "round",
							"stroke-linejoin": "round",
							"stroke-width": "2",
							d: "M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z",
						}),
						e("path", {
							"stroke-linecap": "round",
							"stroke-linejoin": "round",
							"stroke-width": "2",
							d: "M15 11a3 3 0 11-6 0 3 3 0 016 0z",
						}),
					]
				),
			],
			-1
		)
	),
	Tt = b(() =>
		e(
			"h3",
			{ class: "text-lg font-bold text-gray-900 dark:text-white" },
			"Select Store Location",
			-1
		)
	),
	Vt = b(() =>
		e(
			"p",
			{ class: "text-sm text-gray-500" },
			"Choose a location from the top menu to view inventory.",
			-1
		)
	),
	Wt = [Gt, Tt, Vt],
	qt = { key: 1, class: "h-full flex flex-col" },
	Ot = { class: "flex items-center gap-4 mb-6" },
	Ht = b(() =>
		e(
			"h2",
			{
				class: "text-2xl font-serif font-bold text-gray-900 dark:text-white transition-colors",
			},
			"Collection",
			-1
		)
	),
	Ut = {
		class: "text-xs font-bold uppercase tracking-widest text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 px-3 py-1 rounded-full shadow-sm border border-gray-100 dark:border-gray-700 transition-colors",
	},
	Et = { class: "flex-1 overflow-y-auto pb-20 pr-2 custom-scrollbar" },
	Qt = { key: 0, class: "py-20 text-center" },
	Rt = b(() =>
		e(
			"div",
			{
				class: "animate-spin rounded-full h-8 w-8 border-2 border-gray-900 dark:border-white border-t-transparent mx-auto mb-4",
			},
			null,
			-1
		)
	),
	Jt = b(() =>
		e("span", { class: "text-gray-400 text-sm font-medium" }, "Curating Collection...", -1)
	),
	Kt = [Rt, Jt],
	Xt = {
		key: 1,
		class: "py-20 text-center bg-white dark:bg-gray-900 rounded-2xl border border-dashed border-gray-200 dark:border-gray-700",
	},
	Yt = b(() =>
		e("p", { class: "text-gray-500" }, "No pieces found matching your criteria.", -1)
	),
	Zt = [Yt],
	es = { key: 2, class: "smart-grid" },
	ts = ["onClick"],
	ss = { key: 3, class: "flex justify-center pt-12 pb-12" },
	os = ["disabled"],
	rs = {
		setup(t) {
			const d = R(),
				n = Z(),
				i = m(!1),
				s = m(null),
				c = m([]),
				y = m(0),
				p = 20,
				v = m(!0),
				g = D({
					url: "zevar_core.api.get_pos_items",
					makeParams() {
						const S = n.activeFilters,
							{ in_stock_only: u, out_of_stock_only: x } = S,
							f = B(S, ["in_stock_only", "out_of_stock_only"]);
						return {
							warehouse: d.currentWarehouse,
							page_length: p,
							start: y.value,
							search_term: n.searchQuery,
							filters: JSON.stringify(f),
							in_stock_only: u || !1,
							out_of_stock_only: x || !1,
						};
					},
					onSuccess(u) {
						u.length < p && (v.value = !1),
							y.value === 0 ? (c.value = u) : c.value.push(...u);
					},
				});
			function k() {
				!v.value || g.loading || ((y.value += p), g.fetch());
			}
			function w(u) {
				(s.value = u), (i.value = !0);
			}
			let l = null;
			return (
				M(
					() => [n.searchQuery, n.activeFilters],
					() => {
						l && clearTimeout(l),
							(l = setTimeout(() => {
								(y.value = 0), (v.value = !0), g.fetch();
							}, 400));
					},
					{ deep: !0 }
				),
				M(
					() => d.currentWarehouse,
					(u) => {
						u ? ((y.value = 0), g.fetch()) : (c.value = []);
					},
					{ immediate: !0 }
				),
				(u, x) => (
					o(),
					G(J, null, {
						default: T(() => [
							$(d).currentWarehouse
								? (o(),
								  r("div", qt, [
										e("div", Ot, [
											Ht,
											e("span", Ut, a(c.value.length) + " Items Found ", 1),
										]),
										e("div", Et, [
											$(g).loading && y.value === 0
												? (o(), r("div", Qt, Kt))
												: c.value.length === 0
												? (o(), r("div", Xt, Zt))
												: (o(),
												  r("div", es, [
														(o(!0),
														r(
															F,
															null,
															V(
																c.value,
																(f) => (
																	o(),
																	r(
																		"div",
																		{
																			key: f.item_code,
																			onClick: (S) =>
																				w(f.item_code),
																			class: "group",
																		},
																		[
																			O(
																				Ne,
																				{ item: f },
																				null,
																				8,
																				["item"]
																			),
																		],
																		8,
																		ts
																	)
																)
															),
															128
														)),
												  ])),
											v.value && c.value.length > 0
												? (o(),
												  r("div", ss, [
														e(
															"button",
															{
																onClick: k,
																disabled: $(g).loading,
																class: "px-8 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white rounded-full shadow-sm hover:shadow-md hover:border-gray-900 dark:hover:border-white transition-all text-sm font-bold uppercase tracking-wider disabled:opacity-50",
															},
															a(
																$(g).loading
																	? "Loading..."
																	: "Load More"
															),
															9,
															os
														),
												  ]))
												: h("", !0),
										]),
								  ]))
								: (o(), r("div", Dt, Wt)),
							O(
								Pt,
								{
									show: i.value,
									itemCode: s.value,
									onClose: x[0] || (x[0] = (f) => (i.value = !1)),
								},
								null,
								8,
								["show", "itemCode"]
							),
						]),
						_: 1,
					})
				)
			);
		},
	};
var ls = P(rs, [["__scopeId", "data-v-f6828a1e"]]);
export { ls as default };
