#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click
from colorama import init, Fore, Style

# 初始化colorama
init()

class MCPTool:
    def __init__(self):
        self.mapping_file = None
        self.source_dir = None
        self.output_dir = None

    def load_mapping(self, mapping_file):
        """加载混淆映射文件"""
        if not os.path.exists(mapping_file):
            click.echo(f"{Fore.RED}错误: 映射文件 {mapping_file} 不存在{Style.RESET_ALL}")
            return False
        self.mapping_file = mapping_file
        return True

    def process_file(self, input_file, output_file, reverse=False):
        """处理单个文件"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # TODO: 实现实际的混淆/反混淆逻辑
            # 这里需要根据具体的映射规则来实现
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            click.echo(f"{Fore.GREEN}成功处理文件: {input_file}{Style.RESET_ALL}")
            return True
        except Exception as e:
            click.echo(f"{Fore.RED}处理文件 {input_file} 时出错: {str(e)}{Style.RESET_ALL}")
            return False

    def process_directory(self, source_dir, output_dir, reverse=False):
        """处理整个目录"""
        if not os.path.exists(source_dir):
            click.echo(f"{Fore.RED}错误: 源目录 {source_dir} 不存在{Style.RESET_ALL}")
            return False

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        success_count = 0
        total_count = 0

        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.java'):
                    total_count += 1
                    input_path = os.path.join(root, file)
                    relative_path = os.path.relpath(input_path, source_dir)
                    output_path = os.path.join(output_dir, relative_path)
                    
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    if self.process_file(input_path, output_path, reverse):
                        success_count += 1

        click.echo(f"\n{Fore.GREEN}处理完成: {success_count}/{total_count} 个文件成功处理{Style.RESET_ALL}")
        return True

@click.group()
def cli():
    """MCP工具 - Minecraft代码混淆/反混淆工具"""
    pass

@cli.command()
@click.argument('mapping_file', type=click.Path(exists=True))
@click.argument('source_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
def deobfuscate(mapping_file, source_dir, output_dir):
    """反混淆代码"""
    tool = MCPTool()
    if tool.load_mapping(mapping_file):
        tool.process_directory(source_dir, output_dir, reverse=True)

@cli.command()
@click.argument('mapping_file', type=click.Path(exists=True))
@click.argument('source_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
def obfuscate(mapping_file, source_dir, output_dir):
    """混淆代码"""
    tool = MCPTool()
    if tool.load_mapping(mapping_file):
        tool.process_directory(source_dir, output_dir, reverse=False)

if __name__ == '__main__':
    cli() 