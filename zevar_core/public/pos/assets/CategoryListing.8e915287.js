import {
	_ as J,
	x as w,
	o as l,
	k as i,
	l as e,
	n as g,
	t as u,
	u as _,
	q as C,
	B as O,
	C as Q,
	i as p,
	j as Y,
	y as X,
	H as Z,
	D as V,
	G as n,
	z as ee,
	m as y,
	Q as k,
	F as B,
	A as R,
	I as te,
	R as se,
	p as oe,
	r as ae,
	S as N,
	b as re,
} from "./vendor.b4720657.js";
import { H as le, P as ne } from "./ProductModal.47c14e3f.js";
import { a as ie } from "./ui.7e64e684.js";
const P = (t) => (O("data-v-e7571760"), (t = t()), Q(), t),
	ce = {
		class: "relative rounded-2xl overflow-hidden bg-gray-50 aspect-square mb-3 border border-gray-100 group-hover:border-[#C9A962] transition-all group-hover:shadow-lg",
	},
	ue = ["src", "alt"],
	de = { key: 1, class: "flex items-center justify-center h-full text-6xl opacity-40" },
	ge = { class: "absolute top-3 left-3 flex flex-col gap-2" },
	pe = {
		key: 0,
		class: "px-2.5 py-1 bg-[#8B6914] text-white text-[10px] font-bold uppercase tracking-wider rounded-md",
	},
	me = {
		key: 1,
		class: "px-2.5 py-1 bg-emerald-500 text-white text-[10px] font-bold uppercase tracking-wider rounded-md",
	},
	he = {
		key: 2,
		class: "px-2.5 py-1 bg-blue-500 text-white text-[10px] font-bold uppercase tracking-wider rounded-md",
	},
	ve = P(() =>
		e(
			"button",
			{
				class: "absolute bottom-3 right-3 w-10 h-10 bg-white rounded-full shadow-md flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity hover:bg-[#8B6914] hover:text-white",
			},
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
							d: "M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z",
						}),
					]
				),
			],
			-1
		)
	),
	xe = { class: "space-y-1.5" },
	ye = {
		class: "font-medium text-sm text-gray-900 line-clamp-2 min-h-[2.5rem] group-hover:text-[#8B6914] transition-colors",
	},
	fe = { class: "flex items-center gap-2 text-xs text-gray-500" },
	be = { key: 0 },
	_e = { key: 1, class: "w-1 h-1 rounded-full bg-gray-300" },
	we = { key: 2 },
	ke = { key: 0, class: "flex items-center gap-3 text-xs" },
	$e = { key: 0, class: "text-gray-600" },
	Ce = P(() => e("span", { class: "font-medium" }, "Gross:", -1)),
	Be = { key: 1, class: "text-red-600" },
	Re = P(() => e("span", { class: "font-medium" }, "Stone:", -1)),
	Pe = { key: 2, class: "text-[#8B6914] font-medium" },
	Se = P(() => e("span", null, "Net:", -1)),
	je = { class: "pt-2 border-t border-gray-100" },
	qe = { class: "flex items-baseline gap-2" },
	Fe = { class: "text-lg font-bold text-gray-900 font-serif" },
	De = { key: 0, class: "text-sm text-gray-400 line-through" },
	Me = { key: 0, class: "text-xs text-gray-400 mt-0.5" },
	Ve = {
		props: { product: { type: Object, required: !0 } },
		emits: ["click"],
		setup(t) {
			const f = t,
				S = w(
					() => f.product.gross_weight || f.product.stone_weight || f.product.net_weight
				);
			function b(m) {
				return m
					? new Intl.NumberFormat("en-US", {
							style: "currency",
							currency: "USD",
							minimumFractionDigits: 0,
							maximumFractionDigits: 0,
					  }).format(m)
					: "$0";
			}
			function s(m) {
				return m ? `${parseFloat(m).toFixed(2)}g` : "0g";
			}
			return (m, h) => (
				l(),
				i(
					"div",
					{
						class: "group cursor-pointer",
						onClick: h[0] || (h[0] = (j) => m.$emit("click", t.product)),
					},
					[
						e("div", ce, [
							t.product.image
								? (l(),
								  i(
										"img",
										{
											key: 0,
											src: t.product.image,
											alt: t.product.item_name,
											class: "w-full h-full object-cover group-hover:scale-105 transition-transform duration-500",
										},
										null,
										8,
										ue
								  ))
								: (l(), i("div", de, " \u{1F48E} ")),
							e("div", ge, [
								t.product.is_featured
									? (l(), i("span", pe, "Featured"))
									: g("", !0),
								t.product.is_trending
									? (l(), i("span", me, "Trending"))
									: g("", !0),
								t.product.stock_qty > 0
									? (l(), i("span", he, "In Stock"))
									: g("", !0),
							]),
							ve,
						]),
						e("div", xe, [
							e("h3", ye, u(t.product.item_name), 1),
							e("div", fe, [
								t.product.metal
									? (l(), i("span", be, u(t.product.metal), 1))
									: g("", !0),
								t.product.metal && t.product.purity
									? (l(), i("span", _e))
									: g("", !0),
								t.product.purity
									? (l(), i("span", we, u(t.product.purity), 1))
									: g("", !0),
							]),
							_(S)
								? (l(),
								  i("div", ke, [
										t.product.gross_weight
											? (l(),
											  i("span", $e, [
													Ce,
													C(" " + u(s(t.product.gross_weight)), 1),
											  ]))
											: g("", !0),
										t.product.stone_weight
											? (l(),
											  i("span", Be, [
													Re,
													C(" " + u(s(t.product.stone_weight)), 1),
											  ]))
											: g("", !0),
										t.product.net_weight
											? (l(),
											  i("span", Pe, [
													Se,
													C(" " + u(s(t.product.net_weight)), 1),
											  ]))
											: g("", !0),
								  ]))
								: g("", !0),
							e("div", je, [
								e("div", qe, [
									e("span", Fe, u(b(t.product.price)), 1),
									t.product.msrp && t.product.msrp > t.product.price
										? (l(), i("span", De, u(b(t.product.msrp)), 1))
										: g("", !0),
								]),
								t.product.jewelry_type
									? (l(), i("p", Me, u(t.product.jewelry_type), 1))
									: g("", !0),
							]),
						]),
					]
				)
			);
		},
	};
var Ue = J(Ve, [["__scopeId", "data-v-e7571760"]]);
const Ie = { class: "max-w-7xl mx-auto px-6 py-3" },
	Ne = C("Home"),
	He = e(
		"svg",
		{ class: "w-4 h-4", fill: "none", stroke: "currentColor", viewBox: "0 0 24 24" },
		[
			e("path", {
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "2",
				d: "M9 5l7 7-7 7",
			}),
		],
		-1
	),
	Ae = { class: "absolute inset-0 opacity-10" },
	Te = ["src"],
	ze = { class: "relative max-w-7xl mx-auto px-6 h-full flex flex-col justify-center" },
	Ge = { class: "max-w-7xl mx-auto px-6 py-10" },
	Ke = { class: "flex gap-8" },
	Ee = { class: "w-64 flex-shrink-0 hidden lg:block" },
	Le = { class: "sticky top-6 space-y-6" },
	We = { class: "space-y-2" },
	Je = e("span", null, "All Prices", -1),
	Oe = e("span", null, "Under $500", -1),
	Qe = e("span", null, "$500 - $1,000", -1),
	Ye = e("span", null, "$1,000 - $2,500", -1),
	Xe = e("span", null, "$2,500+", -1),
	Ze = { class: "space-y-2" },
	et = ["value"],
	tt = { class: "space-y-2" },
	st = ["value"],
	ot = { class: "flex-1" },
	at = { class: "flex items-center justify-between mb-6" },
	rt = e("option", { value: "featured" }, "Featured", -1),
	lt = e("option", { value: "price-asc" }, "Price: Low to High", -1),
	nt = e("option", { value: "price-desc" }, "Price: High to Low", -1),
	it = e("option", { value: "newest" }, "Newest First", -1),
	ct = [rt, lt, nt, it],
	ut = { key: 0, class: "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6" },
	dt = { key: 1, class: "text-center py-16" },
	gt = e(
		"svg",
		{
			class: "w-16 h-16 mx-auto text-gray-300 mb-4",
			fill: "none",
			stroke: "currentColor",
			viewBox: "0 0 24 24",
		},
		[
			e("path", {
				"stroke-linecap": "round",
				"stroke-linejoin": "round",
				"stroke-width": "1.5",
				d: "M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4",
			}),
		],
		-1
	),
	pt = { key: 2, class: "grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6" },
	xt = {
		setup(t) {
			const f = se(),
				S = oe(),
				b = ie(),
				s = p(b.isDark);
			function m() {
				b.toggleTheme(), (s.value = b.isDark);
			}
			const h = w(() => {
					var a;
					return ((a = f.params.category) == null ? void 0 : a.toLowerCase()) || "all";
				}),
				j = w(() => f.params.category || "All Jewelry"),
				$ = p(!0),
				q = p([]),
				U = p(0),
				F = p(!1),
				D = p(null),
				I = p("featured"),
				c = p({ priceRange: "all", metals: [], purities: [] }),
				H = p(["Yellow Gold", "White Gold", "Rose Gold", "Platinum", "Silver"]),
				A = p(["10K", "14K", "18K", "22K", "24K"]),
				T = w(
					() =>
						({
							rings: "https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=1200&q=80",
							earrings:
								"https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?w=1200&q=80",
							necklaces:
								"https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=1200&q=80",
							chains: "https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?w=1200&q=80",
							bracelets:
								"https://images.unsplash.com/photo-1611591437281-460bfbe1220a?w=1200&q=80",
							pendants:
								"https://images.unsplash.com/photo-1603561591411-07134e71a2a9?w=1200&q=80",
							gold: "https://images.unsplash.com/photo-1610375461246-83df859d849d?w=1200&q=80",
							diamond:
								"https://images.unsplash.com/photo-1605100804763-247f67b3557e?w=1200&q=80",
						}[h.value] ||
						"https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=1200&q=80")
				),
				z = w(
					() =>
						({
							rings: "Discover our exquisite collection of engagement rings, wedding bands, and fashion rings",
							earrings: "Elegant studs, hoops, and drop earrings for every occasion",
							necklaces:
								"From delicate chains to statement pieces that capture attention",
							chains: "Classic gold and diamond chains crafted to perfection",
							bracelets: "Timeless bracelets and bangles to adorn your wrists",
							pendants: "Beautiful pendants that tell your unique story",
							gold: "Premium gold jewelry in various purities and designs",
							diamond: "Brilliant diamonds set in exquisite designs",
						}[h.value] || "Explore our premium jewelry collection")
				);
			function G() {
				const a = {},
					r = {
						rings: "Rings",
						earrings: "Earrings",
						necklaces: "Necklaces",
						chains: "Chains",
						bracelets: "Bracelets",
						pendants: "Pendants",
						gold: null,
						diamond: null,
					},
					d = h.value.toLowerCase();
				return (
					d === "gold"
						? (a.custom_metal_type = ["like", "%Gold%"])
						: d === "diamond"
						? (a.custom_product_type = ["like", "%Diamond%"])
						: r[d] && (a.custom_jewelry_type = r[d]),
					c.value.metals.length > 0 && (a.custom_metal_type = c.value.metals),
					c.value.purities.length > 0 && (a.custom_purity = c.value.purities),
					a
				);
			}
			const K = Y({
				url: "zevar_core.api.get_pos_items",
				makeParams() {
					const a = G();
					let r = null,
						d = null;
					const o = c.value.priceRange;
					o === "0-500"
						? (d = 500)
						: o === "500-1000"
						? ((r = 500), (d = 1e3))
						: o === "1000-2500"
						? ((r = 1e3), (d = 2500))
						: o === "2500+" && (r = 2500);
					const x = { start: 0, page_length: 100, filters: JSON.stringify(a) };
					return r && (x.min_price = r), d && (x.max_price = d), x;
				},
				onSuccess(a) {
					(q.value = a || []),
						(U.value = (a == null ? void 0 : a.length) || 0),
						($.value = !1);
				},
				onError(a) {
					console.error("Failed to load items:", a), ($.value = !1);
				},
			});
			function M() {
				($.value = !0), K.fetch();
			}
			function v() {
				M();
			}
			function E(a) {
				S.push(`/catalogues/${a}`);
			}
			function L(a) {
				(D.value = a.item_code), (F.value = !0);
			}
			function W(a) {
				console.log("Search:", a);
			}
			return (
				X(h, () => {
					M();
				}),
				Z(() => {
					M();
				}),
				(a, r) => {
					const d = ae("router-link");
					return (
						l(),
						i(
							"div",
							{
								class: n([
									"min-h-screen",
									s.value ? "bg-[#0a0a0a] text-white" : "bg-white text-gray-900",
								]),
							},
							[
								V(
									le,
									{
										isDark: s.value,
										activeCategory: _(h),
										onToggleTheme: m,
										onSearch: W,
										onSelectCategory: E,
									},
									null,
									8,
									["isDark", "activeCategory"]
								),
								e(
									"div",
									{
										class: n([
											"border-b",
											s.value
												? "bg-[#111] border-white/5"
												: "bg-gray-50 border-gray-200",
										]),
									},
									[
										e("div", Ie, [
											e(
												"div",
												{
													class: n([
														"flex items-center gap-2 text-sm",
														s.value
															? "text-gray-400"
															: "text-gray-600",
													]),
												},
												[
													V(
														d,
														{
															to: "/catalogues",
															class: "hover:text-[#C9A962]",
														},
														{ default: ee(() => [Ne]), _: 1 }
													),
													He,
													e(
														"span",
														{
															class: n([
																"font-medium capitalize",
																s.value
																	? "text-white"
																	: "text-gray-900",
															]),
														},
														u(_(j)),
														3
													),
												],
												2
											),
										]),
									],
									2
								),
								e(
									"div",
									{
										class: n([
											"relative h-60 overflow-hidden",
											s.value
												? "bg-gradient-to-br from-[#111] to-[#1a1a1a]"
												: "bg-gradient-to-br from-[#faf5f0] to-[#e8ddd0]",
										]),
									},
									[
										e("div", Ae, [
											e(
												"img",
												{ src: _(T), class: "w-full h-full object-cover" },
												null,
												8,
												Te
											),
										]),
										e("div", ze, [
											e(
												"h1",
												{
													class: n([
														"text-4xl md:text-5xl font-serif font-bold mb-2 capitalize",
														s.value ? "text-white" : "text-gray-900",
													]),
												},
												u(_(j)),
												3
											),
											e(
												"p",
												{
													class: n([
														"text-lg font-light",
														s.value
															? "text-gray-400"
															: "text-gray-600",
													]),
												},
												u(_(z)),
												3
											),
										]),
									],
									2
								),
								e("div", Ge, [
									e("div", Ke, [
										e("aside", Ee, [
											e("div", Le, [
												e(
													"div",
													{
														class: n([
															"border-b pb-5",
															s.value
																? "border-white/10"
																: "border-gray-200",
														]),
													},
													[
														e(
															"h3",
															{
																class: n([
																	"font-bold mb-3",
																	s.value
																		? "text-white"
																		: "text-gray-900",
																]),
															},
															" Price Range ",
															2
														),
														e("div", We, [
															e(
																"label",
																{
																	class: n([
																		"flex items-center gap-2 text-sm cursor-pointer",
																		s.value
																			? "text-gray-300"
																			: "text-gray-700",
																	]),
																},
																[
																	y(
																		e(
																			"input",
																			{
																				type: "radio",
																				name: "price",
																				value: "all",
																				"onUpdate:modelValue":
																					r[0] ||
																					(r[0] = (o) =>
																						(c.value.priceRange =
																							o)),
																				onChange: v,
																				class: "text-[#8B6914]",
																			},
																			null,
																			544
																		),
																		[[k, c.value.priceRange]]
																	),
																	Je,
																],
																2
															),
															e(
																"label",
																{
																	class: n([
																		"flex items-center gap-2 text-sm cursor-pointer",
																		s.value
																			? "text-gray-300"
																			: "text-gray-700",
																	]),
																},
																[
																	y(
																		e(
																			"input",
																			{
																				type: "radio",
																				name: "price",
																				value: "0-500",
																				"onUpdate:modelValue":
																					r[1] ||
																					(r[1] = (o) =>
																						(c.value.priceRange =
																							o)),
																				onChange: v,
																				class: "text-[#8B6914]",
																			},
																			null,
																			544
																		),
																		[[k, c.value.priceRange]]
																	),
																	Oe,
																],
																2
															),
															e(
																"label",
																{
																	class: n([
																		"flex items-center gap-2 text-sm cursor-pointer",
																		s.value
																			? "text-gray-300"
																			: "text-gray-700",
																	]),
																},
																[
																	y(
																		e(
																			"input",
																			{
																				type: "radio",
																				name: "price",
																				value: "500-1000",
																				"onUpdate:modelValue":
																					r[2] ||
																					(r[2] = (o) =>
																						(c.value.priceRange =
																							o)),
																				onChange: v,
																				class: "text-[#8B6914]",
																			},
																			null,
																			544
																		),
																		[[k, c.value.priceRange]]
																	),
																	Qe,
																],
																2
															),
															e(
																"label",
																{
																	class: n([
																		"flex items-center gap-2 text-sm cursor-pointer",
																		s.value
																			? "text-gray-300"
																			: "text-gray-700",
																	]),
																},
																[
																	y(
																		e(
																			"input",
																			{
																				type: "radio",
																				name: "price",
																				value: "1000-2500",
																				"onUpdate:modelValue":
																					r[3] ||
																					(r[3] = (o) =>
																						(c.value.priceRange =
																							o)),
																				onChange: v,
																				class: "text-[#8B6914]",
																			},
																			null,
																			544
																		),
																		[[k, c.value.priceRange]]
																	),
																	Ye,
																],
																2
															),
															e(
																"label",
																{
																	class: n([
																		"flex items-center gap-2 text-sm cursor-pointer",
																		s.value
																			? "text-gray-300"
																			: "text-gray-700",
																	]),
																},
																[
																	y(
																		e(
																			"input",
																			{
																				type: "radio",
																				name: "price",
																				value: "2500+",
																				"onUpdate:modelValue":
																					r[4] ||
																					(r[4] = (o) =>
																						(c.value.priceRange =
																							o)),
																				onChange: v,
																				class: "text-[#8B6914]",
																			},
																			null,
																			544
																		),
																		[[k, c.value.priceRange]]
																	),
																	Xe,
																],
																2
															),
														]),
													],
													2
												),
												e(
													"div",
													{
														class: n([
															"border-b pb-5",
															s.value
																? "border-white/10"
																: "border-gray-200",
														]),
													},
													[
														e(
															"h3",
															{
																class: n([
																	"font-bold mb-3",
																	s.value
																		? "text-white"
																		: "text-gray-900",
																]),
															},
															" Metal ",
															2
														),
														e("div", Ze, [
															(l(!0),
															i(
																B,
																null,
																R(
																	H.value,
																	(o) => (
																		l(),
																		i(
																			"label",
																			{
																				key: o,
																				class: n([
																					"flex items-center gap-2 text-sm cursor-pointer",
																					s.value
																						? "text-gray-300"
																						: "text-gray-700",
																				]),
																			},
																			[
																				y(
																					e(
																						"input",
																						{
																							type: "checkbox",
																							value: o,
																							"onUpdate:modelValue":
																								r[5] ||
																								(r[5] =
																									(
																										x
																									) =>
																										(c.value.metals =
																											x)),
																							onChange:
																								v,
																							class: "text-[#8B6914]",
																						},
																						null,
																						40,
																						et
																					),
																					[
																						[
																							N,
																							c.value
																								.metals,
																						],
																					]
																				),
																				e(
																					"span",
																					null,
																					u(o),
																					1
																				),
																			],
																			2
																		)
																	)
																),
																128
															)),
														]),
													],
													2
												),
												e(
													"div",
													{
														class: n([
															"border-b pb-5",
															s.value
																? "border-white/10"
																: "border-gray-200",
														]),
													},
													[
														e(
															"h3",
															{
																class: n([
																	"font-bold mb-3",
																	s.value
																		? "text-white"
																		: "text-gray-900",
																]),
															},
															" Purity ",
															2
														),
														e("div", tt, [
															(l(!0),
															i(
																B,
																null,
																R(
																	A.value,
																	(o) => (
																		l(),
																		i(
																			"label",
																			{
																				key: o,
																				class: n([
																					"flex items-center gap-2 text-sm cursor-pointer",
																					s.value
																						? "text-gray-300"
																						: "text-gray-700",
																				]),
																			},
																			[
																				y(
																					e(
																						"input",
																						{
																							type: "checkbox",
																							value: o,
																							"onUpdate:modelValue":
																								r[6] ||
																								(r[6] =
																									(
																										x
																									) =>
																										(c.value.purities =
																											x)),
																							onChange:
																								v,
																							class: "text-[#8B6914]",
																						},
																						null,
																						40,
																						st
																					),
																					[
																						[
																							N,
																							c.value
																								.purities,
																						],
																					]
																				),
																				e(
																					"span",
																					null,
																					u(o),
																					1
																				),
																			],
																			2
																		)
																	)
																),
																128
															)),
														]),
													],
													2
												),
											]),
										]),
										e("main", ot, [
											e("div", at, [
												e(
													"p",
													{
														class: n(
															s.value
																? "text-gray-400"
																: "text-gray-600"
														),
													},
													u(U.value) + " products ",
													3
												),
												y(
													e(
														"select",
														{
															"onUpdate:modelValue":
																r[7] ||
																(r[7] = (o) => (I.value = o)),
															onChange: v,
															class: n(
																s.value
																	? "px-4 py-2 border border-white/10 rounded-lg text-sm bg-[#1a1a1a] text-white focus:border-[#C9A962] focus:ring-1 focus:ring-[#C9A962]"
																	: "px-4 py-2 border border-gray-200 rounded-lg text-sm focus:border-[#8B6914] focus:ring-1 focus:ring-[#8B6914]"
															),
														},
														ct,
														34
													),
													[[te, I.value]]
												),
											]),
											$.value
												? (l(),
												  i("div", ut, [
														(l(),
														i(
															B,
															null,
															R(8, (o) =>
																e(
																	"div",
																	{
																		key: o,
																		class: "animate-pulse",
																	},
																	[
																		e(
																			"div",
																			{
																				class: n([
																					"rounded-2xl aspect-square mb-3",
																					s.value
																						? "bg-gray-800"
																						: "bg-gray-200",
																				]),
																			},
																			null,
																			2
																		),
																		e(
																			"div",
																			{
																				class: n([
																					"h-4 rounded mb-2",
																					s.value
																						? "bg-gray-800"
																						: "bg-gray-200",
																				]),
																			},
																			null,
																			2
																		),
																		e(
																			"div",
																			{
																				class: n([
																					"h-4 w-2/3 rounded",
																					s.value
																						? "bg-gray-800"
																						: "bg-gray-200",
																				]),
																			},
																			null,
																			2
																		),
																	]
																)
															),
															64
														)),
												  ]))
												: q.value.length === 0
												? (l(),
												  i("div", dt, [
														gt,
														e(
															"p",
															{
																class: n(
																	s.value
																		? "text-gray-400"
																		: "text-gray-500"
																),
															},
															" No products found in this category ",
															2
														),
												  ]))
												: (l(),
												  i("div", pt, [
														(l(!0),
														i(
															B,
															null,
															R(
																q.value,
																(o) => (
																	l(),
																	re(
																		Ue,
																		{
																			key: o.item_code,
																			product: o,
																			onClick: (x) => L(o),
																		},
																		null,
																		8,
																		["product", "onClick"]
																	)
																)
															),
															128
														)),
												  ])),
										]),
									]),
								]),
								V(
									ne,
									{
										show: F.value,
										"item-code": D.value,
										onClose:
											r[8] ||
											(r[8] = (o) => {
												(F.value = !1), (D.value = null);
											}),
									},
									null,
									8,
									["show", "item-code"]
								),
							],
							2
						)
					);
				}
			);
		},
	};
export { xt as default };
