from typing import Any, NamedTuple, Self

import plotly.graph_objects as go  # pyright: ignore[reportMissingTypeStubs]

from ._utils import project_link
from .schema import Symbol, SymbolName, TypeCompletenessReport


class ModuleInfo(NamedTuple):
    parent: SymbolName
    exported: int = 0
    known: int = 0
    ambiguous: int = 0
    unknown: int = 0

    def __add__(self, other: Any) -> Self:
        if isinstance(other, Symbol):
            return self._replace(
                exported=self.exported + 1,
                known=self.known + other.is_type_known,
                ambiguous=self.ambiguous + other.is_type_ambiguous,
                unknown=self.unknown
                + (not (other.is_type_known or other.is_type_ambiguous)),
            )
        elif isinstance(other, self.__class__):
            return self._replace(
                exported=self.exported + other.exported,
                known=self.known + other.known,
                ambiguous=self.ambiguous + other.ambiguous,
                unknown=self.unknown + other.unknown,
            )
        return NotImplemented

    @property
    def completeness_score(self) -> float:
        return 1 if not self.exported else self.known / self.exported


def _collate(report: TypeCompletenessReport) -> dict[SymbolName, ModuleInfo]:
    modules = set(report.modules)
    per_module = {module: ModuleInfo(module.parent) for module in modules}

    for symbol in report.symbols:
        if not symbol.is_exported:
            continue
        mname = symbol.name
        while mname not in modules:
            mname = mname.parent
        per_module[mname] += symbol

    # update parent module totals from their descendants
    for module in sorted(modules, reverse=True)[:-1]:
        per_module[module.parent] += per_module[module]

    return per_module


def to_treemap(
    report: TypeCompletenessReport, generator_link: str | None = None
) -> go.Figure:
    per_module = _collate(report)
    ordered = sorted(per_module)
    info = [per_module[name] for name in ordered]

    title = f"Pyright type completeness report for {report.package_name}"
    attribution = f"Generated with {generator_link or project_link()}"

    return go.Figure(
        data=go.Treemap(
            labels=ordered,
            parents=[i.parent for i in info],
            values=[i.exported for i in info],
            customdata=[
                (
                    i.completeness_score,
                    i.exported,
                    i.known,
                    i.ambiguous,
                    i.unknown,
                )
                for i in info
            ],
            hovertemplate="<br>".join(
                [
                    "<b><u>%{label}</u></b>",
                    "<b>%{customdata[0]:.2%}</b>",
                    "Exported: %{customdata[1]}",
                    "Known: %{customdata[2]}",
                    "Ambiguous: %{customdata[3]}",
                    "Unknown: %{customdata[4]}",
                ]
            )
            + "<extra></extra>",
            marker=go.treemap.Marker(
                colors=[i.completeness_score for i in info], coloraxis="coloraxis"
            ),
        ),
        layout=go.Layout(
            margin=go.layout.Margin(t=75, l=25, r=25, b=25),
            coloraxis=go.layout.Coloraxis(
                colorbar=go.layout.coloraxis.ColorBar(tickformat=".0%"),
                colorscale="rdylgn",
            ),
            # layout trick from plotly/plotly.py#4873, putting the title in
            # an annotation and the footnote in a title gives you much better
            # control over the attribution placement.
            annotations=[
                go.layout.Annotation(
                    showarrow=False,
                    text=title,
                    yref="paper",
                    yanchor="bottom",
                    y=1.04,
                    xref="paper",
                    xanchor="center",
                    x=0.5,
                    font=go.layout.annotation.Font(size=20),
                )
            ],
            legend=go.layout.Legend(
                yanchor="top", y=1, xanchor="right", x=1, borderwidth=1
            ),
            title=go.layout.Title(
                text=attribution,
                yref="container",
                y=0.005,
                xref="paper",
                xanchor="right",
                x=1,
                font=go.layout.title.Font(size=12, style="italic"),
            ),
        ),
    )
