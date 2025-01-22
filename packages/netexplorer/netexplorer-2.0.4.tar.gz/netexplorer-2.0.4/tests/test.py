import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from netexplorer import Crawler, SitesMap



if __name__ == "__main__":
    # crawler = Crawler("https://futureofthe.tech", maxDepth=2, threads=10, maxSites=500)
    # crawler.start()
    sitesMap = SitesMap()
    sitesMap.show()

