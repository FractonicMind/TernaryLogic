#!/usr/bin/env python3
"""
Ternary Logic Framework - Coverage Generation and Analysis

This script generates comprehensive code coverage reports for the TL framework,
including detailed analysis of test coverage across all components.

Created by: Lev Goukassian (ORCID: 0009-0006-5966-1243)
Contact: leogouk@gmail.com

Usage:
    python benchmark/generate_coverage.py [options]
    
Options:
    --html          Generate HTML coverage report
    --xml           Generate XML coverage report  
    --json          Generate JSON coverage report
    --badge         Generate coverage badge data
    --detailed      Include detailed per-function analysis
    --benchmark     Include performance benchmarking
    --all           Generate all report types
"""

import os
import sys
import json
import time
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import coverage
    import pytest
    import psutil
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install: pip install coverage pytest psutil")
    sys.exit(1)


class TLCoverageGenerator:
    """Comprehensive coverage generation and analysis for TL Framework."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.src_dir = project_root / "src"  # Changed to src/ only
        self.tests_dir = project_root / "tests"
        self.coverage_dir = project_root / "coverage_reports"
        self.benchmark_dir = project_root / "benchmark"
        
        # Ensure directories exist
        self.coverage_dir.mkdir(exist_ok=True)
        self.benchmark_dir.mkdir(exist_ok=True)
        
        # Coverage configuration - pointing to src/ only
        self.coverage_config = {
            'source': [str(self.src_dir)],
            'omit': [
                '*/tests/*',
                '*/test_*',
                '*/__pycache__/*',
                '*/venv/*',
                '*/env/*',
                '*/.tox/*'
            ],
            'precision': 2,
            'show_missing': True,
            'skip_covered': False,
            'include_paths': [str(self.src_dir / "*.py")]  # All .py files directly in src/
        }
    
    def run_tests_with_coverage(self) -> Tuple[float, Dict]:
        """Run test suite with coverage measurement."""
        print("🔍 Running test suite with coverage measurement...")
        
        # Initialize coverage
        cov = coverage.Coverage(
            source=self.coverage_config['source'],
            omit=self.coverage_config['omit']
        )
        
        # Start coverage measurement
        cov.start()
        
        # Track performance metrics
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        
        try:
            # Run pytest with coverage
            pytest_args = [
                str(self.tests_dir),
                "-v",
                "--tb=short",
                "-x",  # Stop on first failure
                "--disable-warnings"
            ]
            
            # Run tests
            exit_code = pytest.main(pytest_args)
            
            # Stop coverage measurement
            cov.stop()
            cov.save()
            
            # Calculate performance metrics
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
            
            execution_time = end_time - start_time
            memory_usage = end_memory - start_memory
            
            # Generate coverage report
            coverage_report = self._generate_coverage_data(cov)
            
            # Performance data
            performance_data = {
                'execution_time': round(execution_time, 2),
                'memory_usage': round(memory_usage, 2),
                'test_exit_code': exit_code,
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"✅ Tests completed in {execution_time:.2f}s")
            print(f"📊 Coverage: {coverage_report['total_coverage']:.2f}%")
            print(f"💾 Memory usage: {memory_usage:.1f}MB")
            
            return coverage_report['total_coverage'], {
                'coverage': coverage_report,
                'performance': performance_data
            }
            
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return 0.0, {}
    
    def _generate_coverage_data(self, cov: coverage.Coverage) -> Dict:
        """Generate detailed coverage analysis data."""
        
        # Get coverage data
        coverage_data = cov.get_data()
        
        # Calculate total coverage
        total_statements = 0
        total_missing = 0
        file_coverage = {}
        
        for filename in coverage_data.measured_files():
            # Only include files from src/ directory (not subdirectories)
            if str(self.src_dir) in filename and filename.endswith('.py'):
                # Check if file is directly in src/ (not in subdirectory)
                rel_path = Path(filename).relative_to(self.src_dir)
                if len(rel_path.parts) == 1:  # File is directly in src/
                    analysis = cov._analyze(filename)
                    statements = len(analysis.statements)
                    missing = len(analysis.missing)
                    
                    total_statements += statements
                    total_missing += missing
                    
                    file_coverage[filename] = {
                        'statements': statements,
                        'missing': missing,
                        'coverage': round((statements - missing) / statements * 100, 2) if statements > 0 else 0,
                        'missing_lines': sorted(analysis.missing)
                    }
        
        total_coverage = round((total_statements - total_missing) / total_statements * 100, 2) if total_statements > 0 else 0
        
        return {
            'total_coverage': total_coverage,
            'total_statements': total_statements,
            'total_missing': total_missing,
            'files_covered': len(file_coverage),
            'file_details': file_coverage,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_html_report(self, coverage_data: Dict) -> Path:
        """Generate HTML coverage report."""
        print("📝 Generating HTML coverage report...")
        
        html_dir = self.coverage_dir / "html"
        html_dir.mkdir(exist_ok=True)
        
        # Initialize coverage for HTML generation
        cov = coverage.Coverage(
            source=self.coverage_config['source'],
            omit=self.coverage_config['omit']
        )
        cov.load()
        
        # Generate HTML report
        cov.html_report(
            directory=str(html_dir),
            title="Ternary Logic Framework - Coverage Report",
            show_contexts=True
        )
        
        # Create enhanced HTML index
        self._create_enhanced_html_index(html_dir, coverage_data)
        
        print(f"✅ HTML report generated: {html_dir / 'index.html'}")
        return html_dir / "index.html"
    
    def _create_enhanced_html_index(self, html_dir: Path, coverage_data: Dict):
        """Create enhanced HTML index with additional metrics."""
        
        enhanced_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>TL Framework Coverage Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .header {{ background: linear-gradient(135deg, #1e40af, #3730a3); color: white; padding: 20px; border-radius: 10px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .metric {{ background: #f8fafc; padding: 15px; border-radius: 8px; text-align: center; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #1e40af; }}
        .metric-label {{ color: #6b7280; margin-top: 5px; }}
        .coverage-high {{ color: #059669; }}
        .coverage-medium {{ color: #d97706; }}
        .coverage-low {{ color: #dc2626; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Ternary Logic Framework - Coverage Report</h1>
        <p>Comprehensive code coverage analysis for economic decision-making system</p>
        <p><strong>Generated:</strong> {coverage_data.get('timestamp', 'Unknown')}</p>
    </div>
    
    <div class="metrics">
        <div class="metric">
            <div class="metric-value coverage-{'high' if coverage_data['coverage']['total_coverage'] >= 90 else 'medium' if coverage_data['coverage']['total_coverage'] >= 75 else 'low'}">{coverage_data['coverage']['total_coverage']:.1f}%</div>
            <div class="metric-label">Total Coverage</div>
        </div>
        <div class="metric">
            <div class="metric-value">{coverage_data['coverage']['total_statements']}</div>
            <div class="metric-label">Total Statements</div>
        </div>
        <div class="metric">
            <div class="metric-value">{coverage_data['coverage']['total_missing']}</div>
            <div class="metric-label">Missing Statements</div>
        </div>
        <div class="metric">
            <div class="metric-value">{coverage_data['coverage']['files_covered']}</div>
            <div class="metric-label">Files Covered</div>
        </div>
    </div>
    
    <h2>⚡ Performance Metrics</h2>
    <div class="metrics">
        <div class="metric">
            <div class="metric-value">{coverage_data.get('performance', {}).get('execution_time', 0):.2f}s</div>
            <div class="metric-label">Test Execution Time</div>
        </div>
        <div class="metric">
            <div class="metric-value">{coverage_data.get('performance', {}).get('memory_usage', 0):.1f}MB</div>
            <div class="metric-label">Memory Usage</div>
        </div>
    </div>
    
    <h2>📁 Detailed Coverage by File</h2>
    <p><a href="index_original.html">View Detailed Coverage Report →</a></p>
    
    <div style="margin-top: 40px; padding: 20px; background: #f3f4f6; border-radius: 8px;">
        <h3>🎯 Coverage Targets</h3>
        <ul>
            <li><strong>Minimum Target:</strong> 90% code coverage</li>
            <li><strong>Current Achievement:</strong> {coverage_data['coverage']['total_coverage']:.1f}% </li>
            <li><strong>Quality Assessment:</strong> {'Excellent' if coverage_data['coverage']['total_coverage'] >= 95 else 'Good' if coverage_data['coverage']['total_coverage'] >= 90 else 'Needs Improvement'}</li>
        </ul>
    </div>
</body>
</html>
        """
        
        # Rename original index and save enhanced version
        original_index = html_dir / "index.html"
        if original_index.exists():
            original_index.rename(html_dir / "index_original.html")
        
        with open(html_dir / "index.html", "w") as f:
            f.write(enhanced_html)
    
    def generate_xml_report(self, coverage_data: Dict) -> Path:
        """Generate XML coverage report for CI/CD integration."""
        print("📄 Generating XML coverage report...")
        
        xml_file = self.coverage_dir / "coverage.xml"
        
        # Initialize coverage for XML generation
        cov = coverage.Coverage(
            source=self.coverage_config['source'],
            omit=self.coverage_config['omit']
        )
        cov.load()
        
        # Generate XML report
        cov.xml_report(outfile=str(xml_file))
        
        print(f"✅ XML report generated: {xml_file}")
        return xml_file
    
    def generate_json_report(self, coverage_data: Dict) -> Path:
        """Generate JSON coverage report for programmatic access."""
        print("📋 Generating JSON coverage report...")
        
        json_file = self.coverage_dir / "coverage.json"
        
        # Enhanced JSON report with additional metrics
        json_report = {
            'meta': {
                'version': '1.0.0',
                'timestamp': datetime.now().isoformat(),
                'framework': 'Ternary Logic Framework',
                'creator': 'Lev Goukassian (ORCID: 0009-0006-5966-1243)'
            },
            'summary': {
                'total_coverage': coverage_data['coverage']['total_coverage'],
                'total_statements': coverage_data['coverage']['total_statements'],
                'total_missing': coverage_data['coverage']['total_missing'],
                'files_covered': coverage_data['coverage']['files_covered'],
                'coverage_grade': self._get_coverage_grade(coverage_data['coverage']['total_coverage'])
            },
            'performance': coverage_data.get('performance', {}),
            'files': coverage_data['coverage']['file_details'],
            'thresholds': {
                'excellent': 95.0,
                'good': 90.0,
                'acceptable': 75.0,
                'minimum': 60.0
            }
        }
        
        with open(json_file, 'w') as f:
            json.dump(json_report, f, indent=2)
        
        print(f"✅ JSON report generated: {json_file}")
        return json_file
    
    def generate_badge_data(self, coverage_percentage: float) -> Path:
        """Generate badge data for coverage shields."""
        print("🛡️ Generating coverage badge data...")
        
        badge_file = self.benchmark_dir / "coverage_badge.json"
        
        # Determine badge color based on coverage
        if coverage_percentage >= 95:
            color = "brightgreen"
            status = "excellent"
        elif coverage_percentage >= 90:
            color = "green"
            status = "good"
        elif coverage_percentage >= 75:
            color = "yellowgreen"
            status = "acceptable"
        elif coverage_percentage >= 60:
            color = "yellow"
            status = "needs-improvement"
        else:
            color = "red"
            status = "poor"
        
        badge_data = {
            'schemaVersion': 1,
            'label': 'Coverage',
            'message': f'{coverage_percentage:.0f}%',
            'color': color,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'details': {
                'exact_percentage': coverage_percentage,
                'grade': self._get_coverage_grade(coverage_percentage),
                'framework': 'Ternary Logic Framework'
            }
        }
        
        with open(badge_file, 'w') as f:
            json.dump(badge_data, f, indent=2)
        
        print(f"✅ Badge data generated: {badge_file}")
        return badge_file
    
    def _get_coverage_grade(self, coverage: float) -> str:
        """Get coverage grade based on percentage."""
        if coverage >= 95:
            return "A+"
        elif coverage >= 90:
            return "A"
        elif coverage >= 85:
            return "B+"
        elif coverage >= 80:
            return "B"
        elif coverage >= 75:
            return "C+"
        elif coverage >= 70:
            return "C"
        elif coverage >= 60:
            return "D"
        else:
            return "F"
    
    def generate_detailed_analysis(self, coverage_data: Dict) -> Path:
        """Generate detailed coverage analysis report."""
        print("📊 Generating detailed coverage analysis...")
        
        analysis_file = self.coverage_dir / "detailed_analysis.md"
        
        analysis_content = f"""# Ternary Logic Framework - Detailed Coverage Analysis

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Framework Version:** 1.0.0  
**Total Coverage:** {coverage_data['coverage']['total_coverage']:.2f}%

## 📊 Coverage Summary

| Metric | Value |
|--------|-------|
| **Total Statements** | {coverage_data['coverage']['total_statements']} |
| **Covered Statements** | {coverage_data['coverage']['total_statements'] - coverage_data['coverage']['total_missing']} |
| **Missing Statements** | {coverage_data['coverage']['total_missing']} |
| **Coverage Percentage** | {coverage_data['coverage']['total_coverage']:.2f}% |
| **Coverage Grade** | {self._get_coverage_grade(coverage_data['coverage']['total_coverage'])} |
| **Files Analyzed** | {coverage_data['coverage']['files_covered']} |

## 🎯 Coverage Analysis

### Overall Assessment
- **Status:** {'✅ Excellent' if coverage_data['coverage']['total_coverage'] >= 95 else '👍 Good' if coverage_data['coverage']['total_coverage'] >= 90 else '⚠️ Needs Improvement'}
- **Quality:** {self._get_coverage_grade(coverage_data['coverage']['total_coverage'])} Grade
- **Compliance:** {'Meets' if coverage_data['coverage']['total_coverage'] >= 90 else 'Below'} industry standards (90%+)

### File-by-File Coverage

"""
        
        # Add file details
        for filepath, file_data in coverage_data['coverage']['file_details'].items():
            filename = Path(filepath).name
            coverage_pct = file_data['coverage']
            status_emoji = "✅" if coverage_pct >= 90 else "⚠️" if coverage_pct >= 75 else "❌"
            
            analysis_content += f"""#### {status_emoji} {filename}
- **Coverage:** {coverage_pct:.1f}%  
- **Statements:** {file_data['statements']}  
- **Missing:** {file_data['missing']}  
"""
            
            if file_data['missing_lines']:
                analysis_content += f"- **Missing Lines:** {', '.join(map(str, file_data['missing_lines'][:10]))}{'...' if len(file_data['missing_lines']) > 10 else ''}\n"
            
            analysis_content += "\n"
        
        # Add performance metrics
        if 'performance' in coverage_data:
            perf = coverage_data['performance']
            analysis_content += f"""
## ⚡ Performance Metrics

| Metric | Value |
|--------|-------|
| **Test Execution Time** | {perf.get('execution_time', 0):.2f} seconds |
| **Memory Usage** | {perf.get('memory_usage', 0):.1f} MB |
| **Tests Status** | {'✅ Passed' if perf.get('test_exit_code', 1) == 0 else '❌ Failed'} |

## 📝 Recommendations

### Immediate Actions
"""
            
            if coverage_data['coverage']['total_coverage'] < 90:
                analysis_content += "- 🔴 **Increase coverage to 90%+** for production readiness\n"
            
            if coverage_data['coverage']['total_coverage'] < 95:
                analysis_content += "- ⭐ **Target 95%+ coverage** for excellent quality standards\n"
            
            analysis_content += """
### Testing Focus Areas
- Core TL state transitions (PROCEED/EPISTEMIC_HOLD/HALT)
- Eight Pillars integration points
- Regulatory compliance modules (FATF, IOSCO, Basel III)
- ESG verification accuracy
- Edge cases in Epistemic Hold triggers

## 🏆 Coverage Standards

| Grade | Coverage | Status |
|-------|----------|---------|
| A+ | 95%+ | Excellent - Production Ready |
| A | 90-94% | Good - Acceptable for Production |
| B+ | 85-89% | Above Average - Minor Improvements Needed |
| B | 80-84% | Average - Significant Improvements Needed |
| C+ | 75-79% | Below Average - Major Gaps |
| C | 70-74% | Poor - Extensive Work Required |
| D | 60-69% | Very Poor - Critical Gaps |
| F | <60% | Failing - Not Production Ready |

---

## Contact & Engagement

**Primary Contact**: leogouk@gmail.com  
**Successor Contact**: support@tl-goukassian.org  
(see [Succession Charter](/memorial/SUCCESSION_CHARTER.md))
"""
        
        with open(analysis_file, 'w') as f:
            f.write(analysis_content)
        
        print(f"✅ Detailed analysis generated: {analysis_file}")
        return analysis_file
    
    def generate_all_reports(self) -> Dict[str, Path]:
        """Generate all coverage report types."""
        print("\n" + "="*60)
        print("   TERNARY LOGIC FRAMEWORK - COVERAGE ANALYSIS")
        print("="*60 + "\n")
        
        # Run tests with coverage
        coverage_percentage, coverage_data = self.run_tests_with_coverage()
        
        if coverage_percentage == 0:
            print("❌ Coverage generation failed. No reports generated.")
            return {}
        
        # Generate all report types
        reports = {}
        reports['html'] = self.generate_html_report(coverage_data)
        reports['xml'] = self.generate_xml_report(coverage_data)
        reports['json'] = self.generate_json_report(coverage_data)
        reports['badge'] = self.generate_badge_data(coverage_percentage)
        reports['analysis'] = self.generate_detailed_analysis(coverage_data)
        
        print("\n" + "="*60)
        print(f"   ✅ ALL REPORTS GENERATED SUCCESSFULLY")
        print(f"   📊 Overall Coverage: {coverage_percentage:.1f}%")
        print(f"   📈 Grade: {self._get_coverage_grade(coverage_percentage)}")
        print("="*60 + "\n")
        
        return reports


def main():
    """Main entry point for coverage generation."""
    parser = argparse.ArgumentParser(
        description="Generate coverage reports for Ternary Logic Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python benchmark/generate_coverage.py --all
    python benchmark/generate_coverage.py --html --json
    python benchmark/generate_coverage.py --detailed
        """
    )
    
    parser.add_argument('--html', action='store_true', help='Generate HTML coverage report')
    parser.add_argument('--xml', action='store_true', help='Generate XML coverage report')
    parser.add_argument('--json', action='store_true', help='Generate JSON coverage report')
    parser.add_argument('--badge', action='store_true', help='Generate coverage badge data')
    parser.add_argument('--detailed', action='store_true', help='Generate detailed analysis')
    parser.add_argument('--all', action='store_true', help='Generate all report types')
    
    args = parser.parse_args()
    
    # Default to --all if no options specified
    if not any([args.html, args.xml, args.json, args.badge, args.detailed, args.all]):
        args.all = True
    
    # Initialize generator
    generator = TLCoverageGenerator(project_root)
    
    # Generate requested reports
    if args.all:
        generator.generate_all_reports()
    else:
        coverage_percentage, coverage_data = generator.run_tests_with_coverage()
        
        if coverage_percentage > 0:
            if args.html:
                generator.generate_html_report(coverage_data)
            if args.xml:
                generator.generate_xml_report(coverage_data)
            if args.json:
                generator.generate_json_report(coverage_data)
            if args.badge:
                generator.generate_badge_data(coverage_percentage)
            if args.detailed:
                generator.generate_detailed_analysis(coverage_data)
        else:
            print("❌ No coverage data generated.")
            sys.exit(1)


if __name__ == "__main__":
    main()
