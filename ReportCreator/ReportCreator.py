import argparse
import os
import subprocess
from time import sleep

import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime
import numpy as np
from tex import latex2pdf
from pdflatex import PDFLaTeX

class ReportCreator:
    def createReport(self, numberOfDaysRented, best_listing, best_listing_profit, listing_stats, best_neighbourhood):
        currentDate = str(datetime.now().replace(microsecond=0)).replace(":",
                                                                         "-")
        try:
            os.mkdir("figures")
        except:
            pass

        os.mkdir("figures/" + currentDate)

        N = 6

        for i in range(0, len(listing_stats), N):
            n = min(N, len(listing_stats) - i)
            ind = np.arange(n)  # the x locations for the groups
            width = 0.27  # the width of the bars

            fig = plt.figure(figsize=(15, 8))
            ax = fig.add_subplot(111)

            yvals = [listing_stats[j][2] for j in range(i, i + n)]
            rects1 = ax.bar(ind, yvals, width, color=(0.069, 0.423, 0.548))
            zvals = [listing_stats[j][3] for j in range(i, i + n)]
            rects2 = ax.bar(ind + width, zvals, width, color=(0.069, 0.548, 0.123))
            kvals = [listing_stats[j][4] for j in range(i, i + n)]
            rects3 = ax.bar(ind + width * 2, kvals, width, color=(0.548, 0.069, 0.293))

            ax.set_ylabel("Annual Profit if rented for " + str(numberOfDaysRented) + " days")
            ax.set_xticks(ind + width)
            xLabels = [listing_stats[j][0] + " " + listing_stats[j][1] for j in range(i, i + n)]
            ax.set_xticklabels(xLabels)
            ax.legend((rects1[0], rects2[0], rects3[0]), ('Avg Profit', 'Max Profit', 'Min Profit'))


            def autolabel(rects):
                for rect in rects:
                    h = rect.get_height()
                    ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h,
                            '%d' % int(h),
                            ha='center', va='bottom')

            autolabel(rects1)
            autolabel(rects2)
            autolabel(rects3)

            # plt.show()
            fig.savefig(
                "figures/" + currentDate + "/neighbourhoods-" + str(i) + ".png")

        n = 1
        ind = np.arange(n)  # the x locations for the groups
        width = 0.20  # the width of the bars

        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(111)

        yvals = [best_neighbourhood[2]]
        rects1 = ax.bar(ind, yvals, width, color=(0.069, 0.423, 0.548))
        zvals = [best_neighbourhood[3]]
        rects2 = ax.bar(ind + width, zvals, width, color=(0.069, 0.548, 0.123))
        kvals = [best_neighbourhood[4]]
        rects3 = ax.bar(ind + width * 2, kvals, width,
                        color=(0.548, 0.069, 0.293))

        ax.set_ylabel(
            "Annual Profit if rented for " + str(numberOfDaysRented) + " days")
        ax.set_xticks(ind + width)
        xLabels = [best_neighbourhood[0] + " " + best_neighbourhood[1]]
        ax.set_xticklabels(xLabels)
        ax.legend((rects1[0], rects2[0], rects3[0]),
                  ('Avg Profit', 'Max Profit', 'Min Profit'))

        def autolabel(rects):
            for rect in rects:
                h = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h,
                        '%d' % int(h),
                        ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        autolabel(rects3)

        # plt.show()
        fig.savefig(
            "figures/" + currentDate + "/best-neighbourhood.png")

        content = r'''\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}

\title{Airbnb: Best Properties To Buy}
\author{Report assumes the user will rent out their property for ''' + str(numberOfDaysRented) + r''' days}
\date{Report generated on date}

\begin{document}

\maketitle

\section{Introduction}
This program allows a user to select multiple cities and the number of days in the year the user will rent out their property for. The program will then compare existing Airbnb listings and determine which neighbourhood provides the best profit. The profit formula is as follows: \\

\(profit = price * days\_available - sale\_value * tax\_rate - utilities\)
\\ \\
where \(price\) is the price of the listing, \(days_available\) is the number of days for which the listing is rented out, \(sale_value\) is the value of the property (equal to the average value of its neighbourhood), \(tax_rate\) is the annual property tax (equal to the average tax rate for a residence in the city) and \(utilities\) is the cost of utilities (electricity, heating, water and garbage).

\section{Best Listing}
The most profitable listing on Airbnb in the selected cities is as follows:\\ \\
\textbf{id, name, host\_id, host\_name, city, neighbourhood, latitude, longitude, room\_type, price, minimum\_nights, number\_of\_reviews, last\_review, reviews\_per\_month, calculated\_host\_listings\_count, availability\_365:} \\
'''
        for i in best_listing:
            content += str(i) + ", "

        content += r'''\\ If available for ''' + str(numberOfDaysRented) + r''' days, the property will make '''
        content += "{:.2f}".format(best_listing_profit) + r''' dollars annually. \\'''

        content += r'''\section{Neighbourhoods}
\begin{figure}
  \includegraphics[width=1.0\textwidth]{figures/''' + currentDate + r'''/best-neighbourhood.png}
  \caption{The best neighbourhood to buy in based on average profit.}
  \label{fig:neighbourhood_best_1}
\end{figure} \\ \\
        '''

        for i in range(0, len(listing_stats), N):
            content2 = r'''
  \includegraphics[width=1.0\textwidth]{figures/''' + currentDate + r'''/neighbourhoods-''' + str(i) + r'''.png}
  \caption{}
  \label{fig:n''' + str(i) + r'''}
\end{figure}
'''
            content += content2

        content += r'''\end{document}'''

        # this builds a pdf-file inside a temporary directory
        # pdf = build_pdf(content)
        # print(bytes(pdf)[:10])
        #
        with open('report.tex', 'w') as f:
            f.write(content)

        cmd = ['pdflatex', '-interaction', 'nonstopmode', 'report.tex']
        proc = subprocess.Popen(cmd)
        proc.communicate()

        # retcode = proc.returncode
        # if not retcode == 0:
        #     os.unlink('cover.pdf')
        #     raise ValueError(
        #         'Error {} executing command: {}'.format(retcode, ' '.join(cmd)))

        os.unlink('report.tex')
        os.unlink('report.log')


