#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom LaTeX to text formatter with variations and random choices.

This script provides a specialized version of LatexNodes2Text with custom rules
for converting LaTeX expressions to text with random variations.
"""

import random
import re
from pylatexenc.latexwalker import LatexWalker
from pylatexenc.latex2text import LatexNodes2Text, MacroTextSpec, EnvironmentTextSpec, SpecialsTextSpec, get_default_latex_context_db
from pylatexenc.macrospec import MacroSpec, std_macro


class CustomLatexNodes2Text(LatexNodes2Text):
    """
    Specialized LatexNodes2Text class with custom formatting variations.
    """
    
    def __init__(self, **kwargs):
        # Get default context and add our custom rules
        latex_context = get_default_latex_context_db()
        
        # Add macro parsing specifications first (for argument parsing)
        latex_context.add_context_category(
            'custom-parsing',
            prepend=True,
            macros=self._get_custom_macro_specs(),
            environments=[],
            specials=[]
        )
        
        # Add text conversion specifications (these will override default text conversion)
        # Only for specials (no macros to avoid parsing conflicts)
        latex_context.add_context_category(
            'custom-variations',
            prepend=True,  # Our text rules take precedence  
            macros=[],  # Handle all macros in macro_node_to_text method
            environments=self._get_custom_environments(),
            specials=self._get_custom_specials()
        )
        
        # Initialize parent with our custom context
        super().__init__(latex_context=latex_context, **kwargs)
    
    def _get_custom_macro_specs(self):
        """Get macro parsing specifications for macros that take arguments."""
        return [
            # Square root: optional argument [n] + mandatory argument {x}
            std_macro('sqrt', '[{'),
            
            # Fractions: 2 mandatory arguments {numerator}{denominator}
            std_macro('frac', '{{'),
            std_macro('dfrac', '{{'),
            std_macro('tfrac', '{{'),
            
            # Binomial coefficient: 2 mandatory arguments {n}{k}
            std_macro('binom', '{{'),
            
            # Mathematical functions with one argument
            std_macro('mathrm', '{'),
            std_macro('log', ''),  # \log can be used without arguments
            std_macro('ln', ''),   # \ln can be used without arguments  
            std_macro('sin', ''),  # \sin can be used without arguments
            std_macro('cos', ''),  # \cos can be used without arguments
            std_macro('tan', ''),  # \tan can be used without arguments
            std_macro('lim', ''),  # \lim can be used without arguments
            std_macro('text', '{'),
            std_macro('textbf', '{'),
            std_macro('textit', '{'),
            std_macro('boxed', '{'),
            
            # Greek letters (no arguments, but need MacroSpec to override defaults)
        ] + [std_macro(name, '') for name in [
            'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'varepsilon', 'zeta', 'eta',
            'theta', 'vartheta', 'iota', 'kappa', 'varkappa', 'lambda', 'mu', 'nu',
            'xi', 'pi', 'varpi', 'rho', 'varrho', 'sigma', 'varsigma', 'tau',
            'upsilon', 'phi', 'varphi', 'chi', 'psi', 'omega',
            'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi', 'Pi', 'Sigma',
            'Upsilon', 'Phi', 'Psi', 'Omega',
            # Other symbols that might have default MacroTextSpec
            'infty', 'times', 'cdot', 'pm', 'mp', 'approx', 'sim', 'equiv',
            'subseteq', 'iff', 'mapsto', 'ldots', 'cdots', 'dots',
            # Mathematical operators and relations
            'leq', 'geq', 'neq', 'div', 'subset', 'in', 'cup', 'cap', 'emptyset',
            'to', 'quad', 'qquad', 'sum', 'int', 'lim', 'prod', 'nabla',
            'iint', 'iiint', 'oint', 'mathbb', 'left', 'right', '\\',
            '{', '}', # Literal braces
            'n', # For \n newlines
        ]]
    
    def _get_custom_text_specs(self):
        """Get custom text specifications for simple macros (no argument parsing needed)."""
        return [
            # Basic operators
            MacroTextSpec('times', simplify_repl='*'),
            MacroTextSpec('cdot', simplify_repl='*'),
            
            # Plus/minus symbols
            MacroTextSpec('pm', simplify_repl='+/-'),
            MacroTextSpec('mp', simplify_repl='-/+'),
            
            # Approximation symbols
            MacroTextSpec('approx', simplify_repl='~'),
            MacroTextSpec('sim', simplify_repl='~='),
            
            # Equivalence
            MacroTextSpec('equiv', simplify_repl='==='),
            
            # Set relations
            MacroTextSpec('subseteq', simplify_repl='subset='),
            
            # Logic symbols
            MacroTextSpec('iff', simplify_repl='<=>'),
            MacroTextSpec('mapsto', simplify_repl='|->'),
            
            # Dots
            MacroTextSpec('ldots', simplify_repl='...'),
            MacroTextSpec('cdots', simplify_repl='...'),
            MacroTextSpec('dots', simplify_repl='...'),
        ]
    
    def _get_custom_environments(self):
        """Get custom environment specifications."""
        return []
    
    def _get_custom_specials(self):
        """Get custom specials specifications."""
        return [
            # Angle brackets
            SpecialsTextSpec('\\langle', '<'),
            SpecialsTextSpec('\\rangle', '>'),
        ]
    
    def _custom_sqrt_handler(self, node, l2tobj):
        """Custom handler for sqrt macro with random variations."""
        if not node.nodeargd or not node.nodeargd.argnlist:
            return ""
        
        def needs_parentheses(text):
            """Check if text needs parentheses (has multiple elements/operators)"""
            operators = ['+', '-', '*', '/', '^', ' ']
            return any(op in text for op in operators)
        
        # Random choice for sqrt format
        sqrt_rng = random.randint(0, 1)
        
        # Get the arguments correctly
        if len(node.nodeargd.argnlist) >= 1:
            # Check if we have an optional argument (for nth root)
            if len(node.nodeargd.argnlist) >= 2:
                # Has optional argument [n] and mandatory argument {x}
                if node.nodeargd.argnlist[0] is not None:
                    # nth root
                    root_index = l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]])
                    content = l2tobj.nodelist_to_text([node.nodeargd.argnlist[1]])
                    
                    # Parse root index as number
                    try:
                        radicand = float(root_index)
                    except (ValueError, TypeError):
                        radicand = None

                    if radicand == 2 and sqrt_rng == 0:
                        return f"sqrt({content})"
                    else:
                        # Random choice for exponent format
                        exp_rng = random.randint(0, 1)
                        
                        if radicand is not None:
                            try:
                                inv_radicand = 1.0 / radicand
                                # Check decimal places
                                decimal_part = str(inv_radicand).split('.')[1] if '.' in str(inv_radicand) else ""
                                decimal_rng = random.randint(0, 1)
                                
                                if len(decimal_part) <= 5 and decimal_rng == 0:
                                    exp_value = str(inv_radicand)
                                else:
                                    exp_value = f"(1/{root_index})"
                            except (ZeroDivisionError, ValueError):
                                exp_value = f"(1/{root_index})"
                        else:
                            exp_value = f"(1/{root_index})"

                        if needs_parentheses(content):
                            if exp_rng == 0:
                                return f"({content})^{exp_value}"
                            else:
                                return f"({content})**{exp_value}"
                        else:
                            if exp_rng == 0:
                                return f"{content}^{exp_value}"
                            else:
                                return f"{content}**{exp_value}"
                else:
                    # Optional argument is None, so just square root
                    content = l2tobj.nodelist_to_text([node.nodeargd.argnlist[1]])
                    if sqrt_rng == 0:
                        return f"sqrt({content})"
                    else:
                        exp_rng = random.randint(0, 1)
                        decimal_rng = random.randint(0, 1)

                        if decimal_rng == 0:
                            exp_value = "0.5"
                        else:
                            exp_value = "(1/2)"

                        if needs_parentheses(content):
                            if exp_rng == 0:
                                return f"({content})^{exp_value}"
                            else:
                                return f"({content})**{exp_value}"
                        else:
                            if exp_rng == 0:
                                return f"{content}^{exp_value}"
                            else:
                                return f"{content}**{exp_value}"
            else:
                # No optional argument, just sqrt{x} => sqrt(x) or (x)^(1/2)
                content = l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]])
                if sqrt_rng == 0:
                    return f"sqrt({content})"
                else:
                    exp_rng = random.randint(0, 1)
                    decimal_rng = random.randint(0, 1)

                    if decimal_rng == 0:
                        exp_value = "0.5"
                    else:
                        exp_value = "(1/2)"

                    if needs_parentheses(content):
                        if exp_rng == 0:
                            return f"({content})^{exp_value}"
                        else:
                            return f"({content})**{exp_value}"
                    else:
                        if exp_rng == 0:
                            return f"{content}^{exp_value}"
                        else:
                            return f"{content}**{exp_value}"
        return ""
    
    def _custom_frac_handler(self, node, l2tobj):
        """Custom handler for fractions with parentheses for complex expressions."""
        if not node.nodeargd or len(node.nodeargd.argnlist) < 2:
            return ""
        
        numerator = l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]])
        denominator = l2tobj.nodelist_to_text([node.nodeargd.argnlist[1]])
        
        # Add parentheses for complex expressions
        def is_complex(text):
            """Check if expression is complex (contains operators or multiple terms)"""
            operators = ['+', '-', '*', '/', '^', ' ']
            return any(op in text.strip() for op in operators)
        
        if is_complex(numerator) or is_complex(denominator):
            return f"({numerator})/({denominator})"
        else:
            return f"{numerator}/{denominator}"
    
    def _custom_binom_handler(self, node, l2tobj):
        """Custom handler for binomial coefficients."""
        if not node.nodeargd or len(node.nodeargd.argnlist) < 2:
            return ""
        
        n = l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]])
        k = l2tobj.nodelist_to_text([node.nodeargd.argnlist[1]])
        
        return f"C({n},{k})"
    
    def _custom_mathrm_handler(self, node, l2tobj):
        r"""Custom handler for \mathrm, specifically for 'e'."""
        if not node.nodeargd or not node.nodeargd.argnlist:
            return ""
        
        content = l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]])
        
        # Special case for 'e' (Euler's number)
        if content.strip() == 'e':
            return 'e'
        
        # For other content, just return as is (remove formatting)
        return content
    
    def _custom_boxed_handler(self, node, l2tobj):
        """Custom handler for boxed expressions."""
        if not node.nodeargd or not node.nodeargd.argnlist:
            return ""
        
        content = l2tobj.nodelist_to_text([node.nodeargd.argnlist[0]])
        return f"[{content}]"
    
    def _custom_infty_handler(self, node, l2tobj):
        """Custom handler for infinity symbol with random choice."""
        choices = ['infinity', 'inf', '∞']
        weights = [0.4, 0.4, 0.2]  # 40% infinity, 40% inf, 20% symbol
        return random.choices(choices, weights=weights)[0]
    
    def _custom_pi_handler(self, node, l2tobj):
        """Custom handler for pi symbol with random choice."""
        choices = ['pi', 'π']
        weights = [0.8, 0.2]  # 80% pi, 20% symbol
        return random.choices(choices, weights=weights)[0]
    
    def _greek_letters(self):
        """Return a dictionary of Greek letter names to symbols."""
        return {
            'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε',
            'varepsilon': 'ϵ', 'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'vartheta': 'ϑ',
            'iota': 'ι', 'kappa': 'κ', 'varkappa': 'ϰ', 'lambda': 'λ', 'mu': 'μ',
            'nu': 'ν', 'xi': 'ξ', 'varpi': 'ϖ', 'rho': 'ρ', 'varrho': 'ϱ',
            'sigma': 'σ', 'varsigma': 'ς', 'tau': 'τ', 'upsilon': 'υ', 'phi': 'φ',
            'varphi': 'ϕ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω',
            'Gamma': 'Γ', 'Delta': 'Δ', 'Theta': 'Θ', 'Lambda': 'Λ', 'Xi': 'Ξ',
            'Pi': 'Π', 'Sigma': 'Σ', 'Upsilon': 'Υ', 'Phi': 'Φ', 'Psi': 'Ψ', 'Omega': 'Ω'
        }
    
    def _get_greek_letter_text(self, name):
        """Get the text representation of a Greek letter with random choice."""
        symbol = self._greek_letters().get(name, name)
        choices = [name, symbol]
        weights = [0.8, 0.2]  # 80% spelled out, 20% symbol
        return random.choices(choices, weights=weights)[0]
    
    def _custom_greek_handler(self, name, symbol):
        """Create a handler for Greek letters with random choice."""
        def handler(node, l2tobj):
            choices = [name, symbol]
            weights = [0.8, 0.2]  # 80% spelled out, 20% symbol
            return random.choices(choices, weights=weights)[0]
        return handler
    
    def macro_node_to_text(self, node):
        """Override to handle custom macros and subscripts."""
        # Handle subscripts specially
        if node.macroname == '_' and node.nodeargd and node.nodeargd.argnlist:
            # Convert subscript to underscore notation
            subscript_content = self.nodelist_to_text([node.nodeargd.argnlist[0]])
            return f"_({subscript_content})"
        
        # Handle custom macros that have parsing specs
        if node.macroname == 'sqrt':
            return self._custom_sqrt_handler(node, self)
        elif node.macroname == 'frac' or node.macroname == 'dfrac' or node.macroname == 'tfrac':
            return self._custom_frac_handler(node, self)
        elif node.macroname == 'binom':
            return self._custom_binom_handler(node, self)
        elif node.macroname == 'mathrm':
            return self._custom_mathrm_handler(node, self)
        elif node.macroname == 'boxed':
            return self._custom_boxed_handler(node, self)
        elif node.macroname in ('text', 'textbf', 'textit'):
            # Simple text formatting - just return the content
            if node.nodeargd and node.nodeargd.argnlist:
                return self.nodelist_to_text([node.nodeargd.argnlist[0]])
            return ""
        
        # Handle Greek letters and special symbols
        elif node.macroname == 'pi':
            return self._custom_pi_handler(node, self)
        elif node.macroname == 'infty':
            return self._custom_infty_handler(node, self)
        elif node.macroname in self._greek_letters():
            return self._get_greek_letter_text(node.macroname)
        
        # Handle simple operators and symbols
        elif node.macroname == 'times':
            return '*'
        elif node.macroname == 'cdot':
            return '*'
        elif node.macroname == 'pm':
            return '+/-'
        elif node.macroname == 'mp':
            return '-/+'
        elif node.macroname == 'approx':
            return '~'
        elif node.macroname == 'sim':
            return '~='
        elif node.macroname == 'equiv':
            return '==='
        elif node.macroname == 'subseteq':
            return 'subset='
        elif node.macroname == 'iff':
            return '<=>'
        elif node.macroname == 'mapsto':
            return '|->'
        elif node.macroname in ('ldots', 'cdots', 'dots'):
            return '...'
        
        # Handle additional mathematical symbols and operators
        elif node.macroname == 'leq':
            return '<='
        elif node.macroname == 'geq':
            return '>='
        elif node.macroname == 'neq':
            return '!='
        elif node.macroname == 'div':
            return '÷'
        elif node.macroname == 'subset':
            return '⊂'
        elif node.macroname == 'in':
            return '∈'
        elif node.macroname == 'cup':
            return '∪'
        elif node.macroname == 'cap':
            return '∩'
        elif node.macroname == 'emptyset':
            return '∅'
        elif node.macroname == 'to':
            return '→'
        elif node.macroname == 'quad':
            return '    '  # Four spaces
        elif node.macroname == 'qquad':
            return '        '  # Eight spaces
        elif node.macroname == '\\':
            return '\n'  # Line break
        
        # Handle mathematical functions and operators (keep as-is for now)
        elif node.macroname in ('sum', 'int', 'lim', 'prod', 'nabla', 'iint', 'iiint', 'oint'):
            return f'\\{node.macroname}'
        
        # Handle \mathbb, \left, \right (these need special handling)
        elif node.macroname == 'mathbb':
            if node.nodeargd and node.nodeargd.argnlist:
                content = self.nodelist_to_text([node.nodeargd.argnlist[0]])
                return content  # Just return the letter without special formatting
            return ""
        elif node.macroname in ('left', 'right'):
            return ""  # Ignore delimiters for now
        
        # Handle mathematical functions
        elif node.macroname in ('sin', 'cos', 'tan', 'log', 'ln'):
            return node.macroname
        
        # Handle literal braces
        elif node.macroname == '{':
            return '{'
        elif node.macroname == '}':
            return '}'
        
        # Handle \n (newline)
        elif node.macroname == 'n':
            return '\n'
        
        # For everything else, use parent implementation
        return super().macro_node_to_text(node)
    
    def latex_to_text(self, latex, **parse_flags):
        """Override to ensure our custom context is used during parsing."""
        from pylatexenc import latexwalker
        from pylatexenc.latexnodes import parsers as latexnodes_parsers
        
        # Create LatexWalker with our custom context
        lw = latexwalker.LatexWalker(latex, latex_context=self.latex_context, **parse_flags)
        nodelist, _ = lw.parse_content(latexnodes_parsers.LatexGeneralNodesParser())
        return self.nodelist_to_text(nodelist)


def custom_latex_to_text(latex_text):
    """
    Convert LaTeX text to custom formatted text with variations.
    
    Args:
        latex_text (str): The LaTeX string to convert
        
    Returns:
        str: The converted text with custom formatting
    """
    converter = CustomLatexNodes2Text(strict_latex_spaces="math-all-spaces")
    return converter.latex_to_text(latex_text)


def main():
    """Demonstration of the custom LaTeX formatter."""
    
    # Test cases
    test_cases = [
        r"\sqrt{x+1}",
        r"\sqrt[3]{x+y}",
        r"\frac{x+1}{y-2}",
        r"\binom{n}{k}",
        r"x_{i+1}",
        r"\alpha + \beta = \gamma",
        r"\pi \times \infty",
        r"\pm \sqrt{2}",
        r"\approx 3.14159",
        r"\equiv \text{equivalent}",
        r"\langle x \rangle",
        r"\ldots \text{ and so on}",
        r"\mathrm{e}^{i\pi}",
        r"\Gamma(\alpha) \cdot \Delta",
        r"\[Every \] $time$ \n\n\(it\)\n\n \boxed{wants} to answer?",
        r"\frac{3}{4} + \frac{1}{2} = \frac{5}{4}",
        r"\frac{x^2 + 1}{2\sqrt{x^2 + 1}}",
        r"\sqrt{x^2 + 1}",
        r"\sqrt[3]{x^3 + y^3}",
        r"\alpha + \beta = \gamma",
        r"\pi r^2",
        r"x \leq y \geq z",
        r"a \neq b \approx c",
        r"\infty \pm \times \div",
        r"\sum_{i=1}^{n} x_i",
        r"\int_{0}^{1} x dx",
        r"\int_{-\infty}^{\infty} e^{-x^2} dx",
        r"\sin(x) + \cos(y) + \tan(z)",
        r"\log_{10}(x) + \ln(y)",
        r"\lim_{x \to \infty} \frac{1}{x}",
        r"x \in \mathbb{R} \cap \mathbb{Q}",
        r"A \subset B \subseteq C",
        r"\emptyset \cup \{1,2,3\}",
        r"\frac{d}{dx}\left(\frac{x^2 + 1}{x - 1}\right)",
        r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
        r"\int_0^1 \frac{x^n}{n!} dx = \frac{1}{(n+1)!}",
        r"The answer is \boxed{\frac{5}{4}}",
        r"x = \boxed{-2} or x = \boxed{-3}",
        r"\boxed{x = \boxed{5}} and y = \boxed{10}",
        r"\text{Hello} \mathrm{World}",
        r"\textbf{Bold} \textit{Italic}",
        r"a \quad b \qquad c",
        r"Line 1 \\ Line 2",
        r"\sqrt{\frac{a^2 + b^2}{c^2 + d^2}}",
        r"\sum_{i=1}^{n} \frac{x_i^2}{\sqrt{y_i}}",
        r"\int_{-\infty}^{\infty} \frac{e^{-x^2/2}}{\sqrt{2\pi}} dx",
        r"\frac{d[A]}{dt} = -k[A]^n",
        r"[A](t) = \frac{[A]_0}{1 + k[A]_0 t}",
        r"t_{1/2} = \frac{1}{k[A]_0}",
    ]
    
    print("Custom LaTeX to Text Converter Demo")
    print("=" * 50)
    
    for i, latex in enumerate(test_cases, 1):
        print(f"\nTest {i}: {latex}")
        try:
            # Generate multiple variations to show randomness
            print("Variations:")
            for j in range(3):
                result = custom_latex_to_text(latex)
                print(f"  {j+1}: {result}")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 50)
    print("You can also use it programmatically:")
    print("from format import custom_latex_to_text")
    print("result = custom_latex_to_text(r'\\sqrt{x+1}')")


if __name__ == "__main__":
    main()
