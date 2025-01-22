"""
XXE (XML External Entity) Analysis Package
Provides utilities for detecting and preventing XXE vulnerabilities.
"""

from .core import *

__version__ = '0.1.1'



def cli():
        """Command line interface for XXE scanning"""
        
        parser = argparse.ArgumentParser(description='XXE vulnerability scanner')
        parser.add_argument('file', help='XML file to scan')
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
        args = parser.parse_args()
        
        analyzer = XXEAnalyzer(verbose=args.verbose)
        analyzer.analyze_file(args.file)
        report = analyzer.get_report()
        print(json.dumps(report, indent=2))

def main():
        """Entry point for console script"""
        cli()