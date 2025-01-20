# -*- coding: UTF-8 -*-

import os.path
from typing import Union, Tuple, Optional

import matplotlib
import numpy as np
from anndata import AnnData
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pandas import DataFrame
import seaborn as sns
from ykenan_log import Logger

from ..util import path, collection, type_50_colors, type_20_colors, project_name

log = Logger(f"{project_name}_plot_scatter", level="ERROR")

matplotlib.set_loglevel("error")


def scatter_base(
    df: DataFrame,
    hue: str,
    columns: Tuple[str, str] = ("UMAP1", "UMAP2"),
    hue_order: list = None,
    title: str = None,
    bar_label: str = None,
    cmap: str = "Oranges",
    width: float = 4,
    height: float = 4,
    right: float = 0.9,
    text_fontsize: float = 12,
    start_color_index: int = 0,
    color_step_size: int = 0,
    type_colors: collection = None,
    size: Union[float, collection] = 1.0,
    legend: dict = None,
    number: bool = False,
    is_text: bool = False,
    output: path = None,
    show: bool = True
) -> None:
    if output is None and not show:
        log.info(f"At least one of the `output` and `show` parameters is required")
    else:
        fig, ax = plt.subplots(figsize=(width, height))
        fig.subplots_adjust(right=right)

        if title is not None:
            plt.title(title)

        # scatter
        if number:
            plt.scatter(df[columns[0]], df[columns[1]], c=df[hue], cmap=cmap, s=size)
            color_bar = plt.colorbar(label=bar_label)
            color_bar.set_label(bar_label)
        else:
            __hue_order__ = list(np.sort(list(set(df[hue]))))

            if type_colors is None:
                type_colors = type_20_colors if len(__hue_order__) <= 20 else type_50_colors

            colors = {}

            if legend is not None:
                df.loc[:, "__hue__"] = df[hue].copy()

            i = 0
            for elem in __hue_order__:
                if legend is not None:
                    df.loc[df[df["__hue__"] == elem].index, "__hue__"] = legend[elem]
                    colors.update({legend[elem]: type_colors[start_color_index + i * color_step_size + __hue_order__.index(elem)]})
                else:
                    colors.update(
                        {
                            elem: type_colors[start_color_index + i * color_step_size + __hue_order__.index(elem)]
                        }
                    )
                i += 1

            if legend is not None:
                if hue_order is None:
                    hue_order = list(np.sort(list(set(df["__hue__"]))))
            else:
                if hue_order is None:
                    hue_order = __hue_order__

            sns.scatterplot(
                data=df,
                x=columns[0],
                y=columns[1],
                edgecolor=None,
                palette=colors,
                hue="__hue__" if legend is not None else hue,
                hue_order=hue_order,
                s=size
            )

            if is_text:

                df_anno = df[[hue, columns[0], columns[1]]].groupby(hue, as_index=False).mean()

                for txt, i, j in zip(df_anno[hue], df_anno[columns[0]], df_anno[columns[1]]):
                    plt.annotate(
                        txt,
                        xy=(i, j),
                        xytext=(-10, 0),
                        textcoords="offset points",
                        bbox=dict(
                            boxstyle="round,pad=0.2",
                            fc="white",
                            ec="k",
                            lw=1,
                            alpha=0.8
                        ),
                        fontsize=text_fontsize
                    )

            ax.legend(
                loc="center left",
                bbox_to_anchor=(right, 0.5),
                bbox_transform=fig.transFigure
            )

        # Remove scales and labels on the coordinate axis
        ax.set_xticks([])
        ax.set_yticks([])

        # Remove the bounding box of the coordinate axis
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        ax.set_xlabel(columns[0])
        ax.set_ylabel(columns[1])

        # noinspection DuplicatedCode
        if output is not None:
            output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"
            # plt.savefig(output_pdf, dpi=300)
            with PdfPages(output_pdf) as pdf:
                pdf.savefig(fig)

        if show:
            plt.grid(True)
            plt.show()

        plt.close()


def scatter_atac(
    adata: AnnData,
    columns: Tuple[str, str] = ("UMAP1", "UMAP2"),
    clusters: str = "clusters",
    hue_order: list = None,
    width: float = 4,
    height: float = 4,
    start_color_index: int = 0,
    color_step_size: int = 0,
    type_colors: collection = None,
    size: float = 1.0,
    is_text: bool = False,
    output: path = None,
    show: bool = True
) -> None:
    # DataFrame
    df: DataFrame = adata.obs.copy()
    df[clusters] = df[clusters].astype(str)
    # scatter
    scatter_base(
        df,
        clusters,
        width=width,
        height=height,
        columns=columns,
        size=size,
        hue_order=hue_order,
        start_color_index=start_color_index,
        color_step_size=color_step_size,
        type_colors=type_colors,
        is_text=is_text,
        output=output,
        show=show,
        right=0.75
    )


def scatter_trait(
    trait_adata: AnnData,
    title: str = None,
    bar_label: str = None,
    trait_name: str = "All",
    layers: Union[None, collection] = None,
    columns: Tuple[str, str] = ("UMAP1", "UMAP2"),
    cmap: str = "viridis",
    width: float = 4,
    height: float = 4,
    right: float = 0.9,
    number: bool = True,
    size: Union[float, collection] = 1.0,
    start_color_index: int = 0,
    color_step_size: int = 0,
    type_colors: collection = None,
    is_text: bool = False,
    legend: dict = None,
    output: path = None,
    show: bool = True
) -> None:
    """
    Scatter plot of cell scores for traits/diseases
    :param size:
    :param type_colors:
    :param right:
    :param height:
    :param width:
    :param legend:
    :param color_step_size:
    :param start_color_index:
    :param is_text:
    :param number:
    :param cmap:
    :param bar_label:
    :param title:
    :param columns:
    :param trait_adata: data
    :param trait_name: trait/disease name or All, 'All' show all traits/diseases
    :param layers: Matrix information used in drawing
    :param output: Image output path
    :param show: Whether to display pictures
    :return: None
    """

    data: AnnData = trait_adata.copy()

    # judge layers
    trait_adata_layers = list(data.layers)

    if layers is not None and len(layers) != 0:
        for layer in layers:
            if layer not in trait_adata_layers:
                log.error("The `layers` parameter needs to include in `trait_adata.layers`")
                raise ValueError("The `layers` parameter needs to include in `trait_adata.layers`")

    def trait_plot(trait_: str, atac_cell_df_: DataFrame, layer_: str = None, new_data_: AnnData = None) -> None:
        """
        show plot
        :param trait_: trait name
        :param atac_cell_df_:
        :param layer_: layer
        :param new_data_:
        :return: None
        """
        log.info(f"Plotting scatter {trait_}")
        # get gene score
        trait_score = new_data_[:, trait_].to_df()
        trait_score = trait_score.rename_axis("__barcode__")
        trait_score.reset_index(inplace=True)
        atac_cell_df_ = atac_cell_df_.rename_axis("__barcode__")
        atac_cell_df_.reset_index(inplace=True)
        # trait_score.rename_axis("index")
        df = atac_cell_df_.merge(trait_score, on="__barcode__", how="left")
        # Sort gene scores from small to large
        df.sort_values([trait_], inplace=True)
        scatter_base(
            df,
            trait_,
            title=f"{title} {trait_}" if title is not None else title,
            bar_label=bar_label,
            columns=columns,
            legend=legend,
            cmap=cmap,
            width=width,
            height=height,
            right=right,
            number=number,
            size=size,
            type_colors=type_colors,
            start_color_index=start_color_index,
            color_step_size=color_step_size,
            is_text=is_text,
            output=os.path.join(
                output, f"cell_{trait_}_score_{layer_}.pdf" if layer_ is not None else f"cell_{trait_}_score.pdf"
            ) if output is not None else None,
            show=show
        )

    def handle_plot(layer_: str = None):
        # DataFrame
        atac_cell_df: DataFrame = data.obs.copy()
        atac_cell_df.rename_axis("index", inplace=True)
        trait_list: list = list(data.var_names)

        # judge trait
        if trait_name != "All" and trait_name not in trait_list:
            log.error(f"The {trait_name} trait/disease is not in the trait/disease list (trait_adata.var_names)")
            raise ValueError(f"The {trait_name} trait/disease is not in the trait/disease list (trait_adata.var_names)")

        new_data: AnnData = AnnData(data.layers[layer], var=data.var, obs=data.obs) if layer_ is not None else data

        # plot
        if trait_name == "All":
            for trait in trait_list:
                trait_plot(trait, atac_cell_df, layer_, new_data)
        else:
            trait_plot(trait_name, atac_cell_df, layer_, new_data)

    if layers is None or len(layers) == 0:
        handle_plot()
    else:
        for layer in layers:
            log.info(f"Start {layer}")
            handle_plot(layer)


def volcano_base(
    df: DataFrame,
    x: str = "Log2(Fold change)",
    y: str = "-Log10(P value)",
    hue: str = "type",
    size: int = 3,
    palette: Optional[list] = None,
    width: float = 4,
    height: float = 4,
    y_min: float = 0,
    axh_value: float = -np.log10(1e-3),
    axv_left_value: float = -1,
    axv_right_value: float = 1,
    title: str = None,
    x_name: Optional[str] = None,
    y_name: Optional[str] = None,
    output: path = None,
    show: bool = True
):
    if output is None and not show:
        log.info(f"At least one of the `output` and `show` parameters is required")
    else:

        if palette is None:
            palette = ["#01c5c4", "#686d76", "#ff414d"]

        fig, ax = plt.subplots(figsize=(width, height))

        if title is not None:
            plt.title(title)

        sns.set(style="ticks")
        sns.set_palette(sns.color_palette(palette))
        sns.scatterplot(data=df, x=x, y=y, hue=hue, s=size, ax=ax)
        ax.set_ylim(y_min, max(df[y]) * 1.1)

        if x_name is not None:
            ax.set_xlabel(x_name)

        if y_name is not None:
            ax.set_ylabel(y_name)

        plt.axhline(axh_value, color='grey', linestyle='--')
        plt.axvline(axv_left_value, color='grey', linestyle='--')
        plt.axvline(axv_right_value, color='grey', linestyle='--')

        # noinspection DuplicatedCode
        if output is not None:
            output_pdf = output if output.endswith(".pdf") else f"{output}.pdf"
            # plt.savefig(output_pdf, dpi=300)
            with PdfPages(output_pdf) as pdf:
                pdf.savefig(fig)

        if show:
            plt.grid(True)
            plt.show()

        plt.close()
