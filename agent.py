"""
Code review agent using LangGraph and LangChain-QWQ.
"""
from typing import Dict, Any
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from .prompts import get_code_review_prompt, get_ai_analysis_prompt
from git_ops_domain import GitHubService
import json
import os
import asyncio

# 常量定义
DASHSCOPE_API_BASE = os.getenv("DASHSCOPE_API_BASE", "https://dashscope.aliyuncs.com/compatible-mode/v1")

# Initialize GitHub service
github_service = GitHubService()




@tool
def ai_code_review(filename: str, patch_content: str, file_content: str,static_analysis_results:str) -> Dict[str, Any]:
    """
    使用AI大模型对单个文件的代码变更进行智能分析。
    
    使用场景：
    - 对单个文件的代码变更进行智能分析
    - 发现潜在问题并提供改进建议
    - 检查代码安全性、性能、可维护性等方面
    - 分析代码变更的意图和影响
    
    参数：
    - filename (str): 文件名，例如 "src/main.py"
    - patch_content (str): 文件的diff内容，包含具体的代码变更
    - file_content(str): 提交后的完整文件内容
    
    返回：
    - Dict包含以下信息：
      - issues: 问题列表，每个问题包含line_number(行号)、message(问题描述)、suggestion(修改建议)、severity(严重程度)
    
    示例用法：
    ai_code_review("src/main.py", "@@ -1,3 +1,4 @@\n def func():\n+    # TODO: 添加错误处理\n     return True")
    """
    try:
        # 创建 qwen-coder 模型
        llm = ChatOpenAI(
            temperature=0.1,
            api_key=os.getenv("DASHSCOPE_API_KEY", "default_key"),
            model="qwen3-coder-plus",
            openai_api_base=DASHSCOPE_API_BASE
        )
        
        # 使用专业的分析提示模板
        analysis_prompt = get_ai_analysis_prompt(filename, patch_content,file_content,static_analysis_results)
        
        # 调用模型进行分析
        response = llm.invoke(analysis_prompt)
        analysis_text = response.content if hasattr(response, 'content') else str(response)
        
        # 尝试解析JSON结果
        try:
            analysis_result = json.loads(analysis_text)
            
            # 处理问题列表
            issues = []
            
            if "issues" in analysis_result:
                for issue in analysis_result["issues"]:
                    # 确保每个问题都有必要的字段
                    processed_issue = {
                        "file": filename,  # 添加文件名
                        "line_number": issue.get("line_number", "unknown"),
                        "message": issue.get("message", "问题描述缺失"),
                        "suggestion": issue.get("suggestion", "建议缺失"),
                        "severity": issue.get("severity", "info")
                    }
                    issues.append(processed_issue)
                    
        except json.JSONDecodeError:
            # 如果JSON解析失败，创建简单结果
            issues = [{
                "file": filename,  # 添加文件名
                "line_number": "unknown",
                "message": "代码分析完成",
                "suggestion": "建议检查代码质量",
                "severity": "info"
            }]
        
        # 返回简化的结果，只包含问题列表
        return {
            "issues": issues
        }
        
    except Exception as e:
        return {"error": f"AI代码分析失败: {str(e)}"}


@tool
def pr_comment(repo_owner: str, repo_name: str, pull_number: str, 
               commit_id: str, review_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    将AI代码分析结果作为PR Review提交到GitHub。
    
    使用场景：
    - 仅在处理 pull_request 事件时使用
    - 将AI分析结果自动发布到GitHub PR Review
    - 为代码审查提供智能建议
    - 帮助团队成员了解代码质量和改进方向
    - 自动化代码审查流程
    
    参数：
    - repo_owner (str): GitHub仓库所有者
    - repo_name (str): GitHub仓库名称
    - pull_number (str): PR编号
    - commit_id (str): Git提交的SHA哈希值
    - review_results (Dict[str, Any]): AI分析的结果，包含issues列表
    
    返回：
    - Dict包含以下信息：
      - success: 是否成功发布评论
      - review_id: Review ID（如果成功）
      - message: 操作结果消息
    
    示例用法：
    pr_comment("microsoft", "vscode", "123", "abc123", review_results)
    """
    try:
        # Use GitHub service to post PR review
        result = asyncio.run(github_service.post_pr_review(
            repo_owner, repo_name, pull_number, review_results
        ))
        return result
        
    except Exception as e:
        return {"success": False, "error": f"处理PR Review时出错: {str(e)}"}



## github api  ratelimit 15000 requests per hour 
## https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api?apiVersion=2022-11-28
@tool
def commit_comment(repo_owner: str, repo_name: str, commit_sha: str,
                   review_results: Dict[str, Any],patch_content:str) -> Dict[str, Any]:
    """
    将AI代码分析结果作为commit评论提交到GitHub。
    
    使用场景：
    - 仅在处理 push 事件时使用
    - 将AI分析结果自动发布到GitHub commit评论
    - 为代码提交提供智能建议
    - 帮助开发者了解代码质量和改进方向
    - 自动化代码审查流程
    
    参数：
    - repo_owner (str): GitHub仓库所有者
    - repo_name (str): GitHub仓库名称
    - commit_sha (str): Git提交的SHA哈希值
    - review_results (Dict[str, Any]): AI分析的结果，包含issues列表

    返回：
    - Dict包含以下信息：
      - success: 是否成功发布评论
      - comment_id: 评论ID（如果成功）
      - message: 操作结果消息
    
    示例用法：
    commit_comment("microsoft", "vscode", "abc123", review_results)
    """
    try:
        # Use GitHub service to post commit comments
        result = asyncio.run(github_service.post_commit_comments(
            repo_owner, repo_name, commit_sha, review_results,patch_content
        ))
        
        # 如果成功，返回简单的成功状态
        if result.get("success", False):
            return {"success": True}
        else:
            return result
        
    except Exception as e:
        return {"success": False, "error": f"处理Commit评论时出错: {str(e)}"}


def code_review_agent():
    """
    创建代码审查代理，使用LangGraph和三个核心工具。
    使用create_react_agent实现实时流式输出。
    负责分析代码并提供全面的反馈。
    
    返回:
        CompiledStateGraph: 编译后的代码审查图
    """

    # 创建模型 - 使用 QWQ 模型
    # model = ChatQwQ(
    #     model="qwq-plus",  # 使用通义千问模型
    #     temperature=0.1,
    #     max_tokens=4000,
    #     api_key="default_key"
    # )

    llm = ChatOpenAI(
        temperature=0.1,
        api_key=os.getenv("DASHSCOPE_API_KEY", "default_key"),
        model="qwen-flash",
        openai_api_base=DASHSCOPE_API_BASE
    )
    
    # 定义工具列表
    tools = [
        ai_code_review,
        pr_comment,
        commit_comment
    ]
    
    # 创建系统提示
    system_prompt = get_code_review_prompt()
    
    # 创建代理 - 使用LangGraph版本
    agent = create_react_agent(
        model=llm,  # LangGraph使用model参数而不是llm
        tools=tools,  # 使用三个核心工具
        prompt=system_prompt,  # 使用系统提示字符串
        debug=True,  # 启用调试模式
        version="v2"  # 使用v2版本，支持更好的工具调用
    )
    
    return agent
  