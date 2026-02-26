import {
	_ as D,
	g as v,
	a2 as h,
	a4 as k,
	k as u,
	J as C,
	$ as x,
	a0 as B,
	D as t,
	z as l,
	F as w,
	r,
	o as c,
	l as y,
	q as n,
	t as U,
	b as F,
	n as g,
} from "./vendor.b4720657.js";
const I = {
	name: "InsertVideo",
	props: ["editor"],
	expose: ["openDialog"],
	data() {
		return { addVideoDialog: { url: "", file: null, show: !1 } };
	},
	components: { Button: v, Dialog: h, FileUploader: k },
	methods: {
		openDialog() {
			this.addVideoDialog.show = !0;
		},
		addVideo(i) {
			if (!i) return;
			let safeUrl;
			try {
				safeUrl = new URL(i, window.location.origin).href.replace(/"/g, "&quot;");
			} catch {
				console.warn("Invalid video URL:", i);
				return;
			}
			this.editor.chain().focus().insertContent(`<video src="${safeUrl}" controls></video>`).run(),
				this.reset();
		},
		reset() {
			this.addVideoDialog = this.$options.data().addVideoDialog;
		},
	},
},
	N = { class: "flex items-center space-x-2" },
	S = n(" Remove "),
	b = ["src"],
	A = n(" Insert Video "),
	z = n("Cancel");
function L(i, o, P, R, e, a) {
	const s = r("Button"),
		p = r("FileUploader"),
		V = r("Dialog");
	return (
		c(),
		u(
			w,
			null,
			[
				C(i.$slots, "default", x(B({ onClick: a.openDialog }))),
				t(
					V,
					{
						options: { title: "Add Video" },
						modelValue: e.addVideoDialog.show,
						"onUpdate:modelValue": o[2] || (o[2] = (d) => (e.addVideoDialog.show = d)),
						onAfterLeave: a.reset,
					},
					{
						"body-content": l(() => [
							t(
								p,
								{
									"file-types": "video/*",
									onSuccess:
										o[0] ||
										(o[0] = (d) => (e.addVideoDialog.url = d.file_url)),
								},
								{
									default: l(
										({
											file: d,
											progress: f,
											uploading: _,
											openFileSelector: m,
										}) => [
												y("div", N, [
													t(
														s,
														{ onClick: m },
														{
															default: l(() => [
																n(
																	U(
																		_
																			? `Uploading ${f}%`
																			: e.addVideoDialog.url
																				? "Change Video"
																				: "Upload Video"
																	),
																	1
																),
															]),
															_: 2,
														},
														1032,
														["onClick"]
													),
													e.addVideoDialog.url
														? (c(),
															F(
																s,
																{
																	key: 0,
																	onClick: () => {
																		(e.addVideoDialog.url = null),
																			(e.addVideoDialog.file =
																				null);
																	},
																},
																{ default: l(() => [S]), _: 2 },
																1032,
																["onClick"]
															))
														: g("", !0),
												]),
											]
									),
									_: 1,
								}
							),
							e.addVideoDialog.url
								? (c(),
									u(
										"video",
										{
											key: 0,
											src: e.addVideoDialog.url,
											class: "mt-2 w-full rounded-lg",
											controls: "",
										},
										null,
										8,
										b
									))
								: g("", !0),
						]),
						actions: l(() => [
							t(
								s,
								{
									variant: "solid",
									onClick:
										o[1] || (o[1] = (d) => a.addVideo(e.addVideoDialog.url)),
								},
								{ default: l(() => [A]), _: 1 }
							),
							t(s, { onClick: a.reset }, { default: l(() => [z]), _: 1 }, 8, [
								"onClick",
							]),
						]),
						_: 1,
					},
					8,
					["modelValue", "onAfterLeave"]
				),
			],
			64
		)
	);
}
var q = D(I, [["render", L]]);
export { q as default };
