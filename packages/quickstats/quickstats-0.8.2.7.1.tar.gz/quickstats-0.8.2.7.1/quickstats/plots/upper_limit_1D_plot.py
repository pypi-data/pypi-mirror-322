from typing import Optional, Union, Dict, List

import matplotlib.patches as patches
import matplotlib.lines as lines
import numpy as np
import pandas as pd

from quickstats.plots.template import create_transform
from quickstats.plots import AbstractPlot
from quickstats.utils.common_utils import combine_dict


class UpperLimit1DPlot(AbstractPlot):

    STYLES = {
        'figure': {
            'figsize': (11.111, 10.333),
            'dpi': 72,
            'facecolor': "#FFFFFF"
        },
        'axis': {
            'tick_bothsides': False
        },
        'legend': {
            'fontsize': 22
        },
        'text': {
            'fontsize': 22
        }
    }

    COLOR_PALLETE = {
        '2sigma': 'hh:darkyellow',
        '1sigma': 'hh:lightturquoise',
        'expected': 'k',
        'third': 'k',
        'observed': 'k',
    }

    LABELS = {
        '2sigma': r'Expected limit $\pm 2\sigma$',
        '1sigma': r'Expected limit $\pm 1\sigma$',
        'expected': r'Expected limit',
        'third': 'Third limit',
        'observed': r'Observed limit',
    }

    CONFIG = {
        'top_margin': 2.2,
        'curve_line_styles': {
            'color': 'darkred'
        },
        'curve_fill_styles': {
            'color': 'hh:darkpink'
        },
    }

    def __init__(self, category_df, label_map, line_below=None,
                 color_pallete: Optional[Dict] = None,
                 labels: Optional[Dict] = None,
                 config: Optional[Dict] = None,
                 styles: Optional[Union[Dict, str]] = None,
                 analysis_label_options: Optional[Union[Dict, str]] = None):
        super().__init__(color_pallete=color_pallete,
                         styles=styles,
                         analysis_label_options=analysis_label_options)
        self.category_df = category_df
        self.label_map = label_map
        self.line_below = line_below
        self.curve_data = None

        self.labels = combine_dict(self.LABELS, labels)
        self.config = combine_dict(self.CONFIG, config)

    def get_default_legend_order(self):
        return ["observed", "expected", "third", "one_sigma", "two_sigma", "curve"]        

    def add_curve(self, x, xerrlo=None, xerrhi=None,
                  label: str = "Theory prediction",
                  line_styles: Optional[Dict] = None,
                  fill_styles: Optional[Dict] = None):
        curve_data = {
            'x': x,
            'y': np.arange(0, len(self.category_df.columns)+1),
            'xerrlo': xerrlo,
            'xerrhi': xerrhi,
            'label': label,
            'line_styles': line_styles,
            'fill_styles': fill_styles,
        }
        self.curve_data = curve_data

    def draw_curve(self, ax, data):
        line_styles = data['line_styles']
        fill_styles = data['fill_styles']
        if line_styles is None:
            line_styles = self.config['curve_line_styles']
        if fill_styles is None:
            fill_styles = self.config['curve_fill_styles']
        if (data['xerrlo'] is None) and (data['xerrhi'] is None):
            line_styles['color'] = fill_styles['color']
        handle_line = ax.vlines(
            data['x'], data['y'][0], data['y'][-1], label=data['label'], **line_styles)
        handles = handle_line
        if (data['xerrlo'] is not None) and (data['xerrhi'] is not None):
            handle_fill = ax.fill_betweenx(data['y'], data['xerrlo'], data['xerrhi'],
                                           label=data['label'], **fill_styles)
            handles = (handle_fill, handle_line)
        self.update_legend_handles({'curve': handles})

    def draw(self, logx:bool=False, xlabel:Optional[str]=None, markersize:float=50.,
             draw_observed:bool=True, draw_stat:bool=False, draw_third_column:Optional[str]=None,
             add_text:bool= True, sig_fig:int=2):
        if (draw_observed + draw_stat) > 1:
            raise RuntimeError(
                "draw_observed and draw_stat can not be both True")
        n_category = len(self.category_df.columns)
        ax = self.draw_frame(logx=logx)
        transform = create_transform(transform_x='axis', transform_y='data')

        if draw_observed:
            text_pos = {'observed': 0.775, 'expected': 0.925}
        if draw_stat:
            text_pos = {'expected': 0.775, 'stat': 0.925}
        if (not draw_observed) and (not draw_stat):
            text_pos = {'expected': 0.925}
        if draw_third_column:
            text_pos = {'observed': 0.725, 'expected': 0.825, 'third': 0.925}
        text_styles = self.styles['text'].copy()
        text_styles['verticalalignment']   = 'center'
        text_styles['horizontalalignment'] = 'center'
        for i, category in enumerate(self.category_df):
            df = self.category_df[category]
            # draw observed
            if draw_observed:
                observed_limit = df['obs']
                handle_1 = ax.vlines(observed_limit, i, i+1, colors=self.color_pallete['observed'], linestyles='solid',
                                     zorder=1.1, label=self.labels['observed'] if i == 0 else '')
                handle_2 = ax.scatter(observed_limit, i + 0.5, s=markersize, marker='o',
                                      color=self.color_pallete['observed'], zorder=1.1)
                observed_handle = (handle_1, handle_2)
                if add_text:
                    ax.text(text_pos['observed'], i + 0.5, f"{{:.{sig_fig}f}}".format(observed_limit),
                            transform=transform, **text_styles)
            else:
                observed_handle = None
            # draw stat
            if draw_stat:
                stat_limit = df['stat']
                if add_text:
                    ax.text(text_pos['stat'], i + 0.5, f"({{:.{sig_fig}f}})".format(stat_limit),
                            transform=transform, **text_styles)
            # draw expected
            expected_limit = df['0']
            expected_handle = ax.vlines(expected_limit, i, i + 1, colors=self.color_pallete['expected'], linestyles='dotted',
                                        zorder=1.1, label=self.labels['expected'])
            if add_text:
                ax.text(text_pos['expected'], i + 0.5, f"{{:.{sig_fig}f}}".format(expected_limit),
                        transform=transform, **text_styles)
            # draw third
            if draw_third_column:
                third_limit = df['third']
                third_handle = ax.vlines(third_limit, i, i + 1, colors=self.color_pallete['third'], linestyles='dashed',
                                         zorder=1.1, label=self.labels['third'])
                if add_text:
                    ax.text(text_pos['third'], i + 0.5, f"{{:.{sig_fig}f}}".format(third_limit),
                            transform=transform, **text_styles)
            else:
                third_handle = None
            # draw error band
            two_sigma_handle = ax.fill_betweenx([i, i + 1], df['-2'], df['2'], facecolor=self.color_pallete['2sigma'],
                                                label=self.labels['2sigma'])
            
            one_sigma_handle = ax.fill_betweenx([i, i + 1], df['-1'], df['1'], facecolor=self.color_pallete['1sigma'],
                                                label=self.labels['1sigma'])
            if i == 0:
                handles = {
                    "expected": expected_handle,
                    "one_sigma": one_sigma_handle,
                    "two_sigma": two_sigma_handle,
                }
                for key, handle in [("observed", observed_handle), ("third", third_handle)]:
                    if handle is not None:
                        handles[key] = handle
                self.update_legend_handles(handles)
        xlim = ax.get_xlim()
        ax.set_xlim(xlim[0] - (xlim[1]/0.7 - xlim[1])*0.5, xlim[1]/0.7)
        ax.set_ylim(0, len(self.category_df.columns) +
                    self.config['top_margin'])
        ax.set_yticks(np.arange(n_category) + 0.5, minor=False)
        ax.tick_params(axis="y", which="minor", length=0)
        for axis in ['top', 'bottom', 'left', 'right']:
            ax.spines[axis].set_linewidth(2)
        ax.set_yticklabels([self.label_map[i] for i in self.category_df.columns.to_list()],
                           horizontalalignment='right')
        # draw horizonal dashed lines
        ax.axhline(n_category, color='k', ls='--', lw=1)
        if self.line_below is not None:
            for category in self.line_below:
                position = np.where(
                    np.array(self.category_df.columns, dtype='str') == category)[0]
                if position.shape[0] != 1:
                    raise ValueError(
                        "category `{}` not found in dataframe".format(category))
                ax.axhline(position[0], color='k', ls='--', lw=1)
        if add_text:
            if draw_observed:
                ax.text(text_pos['observed'], n_category + 0.3, 'Obs.',
                        transform=transform, **text_styles)
            if draw_stat:
                ax.text(text_pos['stat'], n_category + 0.3, '(Stat.)',
                        transform=transform, **text_styles)
            if draw_third_column:
                ax.text(text_pos['third'], n_category + 0.3, draw_third_column,
                        transform=transform, **text_styles)
            ax.text(text_pos['expected'], n_category + 0.3, 'Exp.',
                    transform=transform, **text_styles)
        if self.curve_data is not None:
            self.draw_curve(ax, self.curve_data)
        if xlabel is not None:
            ax.set_xlabel(xlabel, **self.styles['xlabel'])
        # border for the legend
        border_leg = patches.Rectangle( (0, 0), 1, 1, facecolor='none', edgecolor='black', linewidth=1)
        self.add_legend_decoration(border_leg, targets=["one_sigma", "two_sigma", "curve"])
        self.draw_legend(ax)
        return ax
