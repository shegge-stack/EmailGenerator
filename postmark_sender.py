#!/usr/bin/env python3
"""
Postmark Email Sender - The Most Powerful 1:1 Messaging System
High-conversion email sending with tracking and analytics
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from loguru import logger
import os
from dataclasses import dataclass

@dataclass
class EmailMetrics:
    """Email performance metrics for conversion tracking."""
    email_id: str
    prospect_email: str
    prospect_name: str
    company_name: str
    sent_at: datetime
    subject: str
    opened_at: Optional[datetime] = None
    clicked_at: Optional[datetime] = None
    replied_at: Optional[datetime] = None
    meeting_booked_at: Optional[datetime] = None
    conversion_score: float = 0.0

class PowerfulPostmarkSender:
    """
    The most powerful 1:1 email sender with conversion optimization.
    
    Features:
    - Postmark integration with tracking
    - Conversion analytics
    - A/B testing
    - Personalization optimization
    - Meeting booking detection
    """
    
    def __init__(self, postmark_api_key: str, from_email: str):
        """Initialize with Postmark credentials."""
        self.api_key = postmark_api_key
        self.from_email = from_email
        self.base_url = "https://api.postmarkapp.com"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Postmark-Server-Token": postmark_api_key
        }
        
        # In-memory storage (use database in production)
        self.email_metrics: List[EmailMetrics] = []
        
    def send_powerful_email(self, 
                           prospect_email: str,
                           prospect_name: str,
                           company_name: str,
                           subject: str,
                           html_body: str,
                           text_body: str,
                           meeting_link: str,
                           sender_name: str,
                           track_opens: bool = True,
                           track_links: bool = True) -> Dict:
        """
        Send a high-conversion 1:1 email with full tracking.
        
        Args:
            prospect_email: Recipient email
            prospect_name: Recipient name
            company_name: Recipient company
            subject: Email subject line
            html_body: HTML email content
            text_body: Plain text email content
            meeting_link: Calendly/booking link
            sender_name: Sender's name
            track_opens: Enable open tracking
            track_links: Enable click tracking
        
        Returns:
            Dict with sending result and tracking info
        """
        try:
            # Generate unique tracking ID
            email_id = str(uuid.uuid4())
            
            # Inject tracking pixels and enhance links
            enhanced_html = self._enhance_email_for_tracking(
                html_body, email_id, meeting_link, track_opens, track_links
            )
            enhanced_text = self._enhance_text_for_tracking(
                text_body, email_id, meeting_link
            )
            
            # Prepare Postmark payload
            payload = {
                "From": f"{sender_name} <{self.from_email}>",
                "To": f"{prospect_name} <{prospect_email}>",
                "Subject": subject,
                "HtmlBody": enhanced_html,
                "TextBody": enhanced_text,
                "MessageStream": "outbound",
                "TrackOpens": track_opens,
                "TrackLinks": "HtmlAndText" if track_links else "None",
                "Metadata": {
                    "email_id": email_id,
                    "prospect_name": prospect_name,
                    "company_name": company_name,
                    "meeting_link": meeting_link,
                    "campaign_type": "1to1_outreach"
                },
                "Headers": [
                    {
                        "Name": "X-Email-ID",
                        "Value": email_id
                    }
                ]
            }
            
            # Send email via Postmark
            response = requests.post(
                f"{self.base_url}/email",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Store metrics for tracking
                metrics = EmailMetrics(
                    email_id=email_id,
                    prospect_email=prospect_email,
                    prospect_name=prospect_name,
                    company_name=company_name,
                    sent_at=datetime.now(),
                    subject=subject
                )
                self.email_metrics.append(metrics)
                
                logger.success(f"Email sent successfully to {prospect_name} at {company_name}")
                
                return {
                    "success": True,
                    "email_id": email_id,
                    "postmark_message_id": result.get("MessageID"),
                    "to": result.get("To"),
                    "submitted_at": result.get("SubmittedAt"),
                    "tracking_url": f"https://yourdomain.com/track/{email_id}",
                    "analytics_dashboard": f"https://yourdomain.com/analytics/{email_id}"
                }
            else:
                error_msg = f"Postmark API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {
                    "success": False,
                    "error": error_msg
                }
                
        except Exception as e:
            logger.error(f"Failed to send email to {prospect_email}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _enhance_email_for_tracking(self, html_body: str, email_id: str, 
                                   meeting_link: str, track_opens: bool, 
                                   track_links: bool) -> str:
        """Enhance HTML email with tracking and conversion optimization."""
        
        enhanced_html = html_body
        
        # Replace meeting link with tracked version
        if track_links and meeting_link:
            tracked_meeting_link = f"https://yourdomain.com/track/click/{email_id}?url={meeting_link}&type=meeting"
            enhanced_html = enhanced_html.replace(meeting_link, tracked_meeting_link)
        
        # Add conversion-optimized elements
        enhanced_html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Personalized Message</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; }}
                .email-content {{ max-width: 600px; margin: 0 auto; }}
                .cta-button {{ 
                    display: inline-block; 
                    padding: 12px 24px; 
                    background: #4f46e5; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 6px; 
                    font-weight: bold;
                    margin: 16px 0;
                }}
                .signature {{ margin-top: 24px; color: #6b7280; }}
            </style>
        </head>
        <body>
            <div class="email-content">
                {enhanced_html}
            </div>
            
            <!-- Conversion tracking pixel -->
            {f'<img src="https://yourdomain.com/track/open/{email_id}" width="1" height="1" style="display:none;" />' if track_opens else ''}
        </body>
        </html>
        """
        
        return enhanced_html
    
    def _enhance_text_for_tracking(self, text_body: str, email_id: str, meeting_link: str) -> str:
        """Enhance plain text email with tracking."""
        
        # Add tracking parameter to meeting link
        if meeting_link:
            tracked_link = f"{meeting_link}?utm_source=email&utm_campaign=1to1_outreach&email_id={email_id}"
            text_body = text_body.replace(meeting_link, tracked_link)
        
        return text_body
    
    def track_email_opened(self, email_id: str) -> bool:
        """Track when email is opened."""
        try:
            for metric in self.email_metrics:
                if metric.email_id == email_id and not metric.opened_at:
                    metric.opened_at = datetime.now()
                    metric.conversion_score += 25  # Opening adds 25 points
                    logger.info(f"Email {email_id} opened by {metric.prospect_name}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error tracking open for {email_id}: {str(e)}")
            return False
    
    def track_link_clicked(self, email_id: str, link_type: str = "general") -> bool:
        """Track when links are clicked."""
        try:
            for metric in self.email_metrics:
                if metric.email_id == email_id:
                    if not metric.clicked_at:
                        metric.clicked_at = datetime.now()
                        if link_type == "meeting":
                            metric.conversion_score += 50  # Meeting link click = 50 points
                        else:
                            metric.conversion_score += 15  # Other links = 15 points
                        logger.info(f"Link clicked in email {email_id} by {metric.prospect_name}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error tracking click for {email_id}: {str(e)}")
            return False
    
    def track_meeting_booked(self, email_id: str) -> bool:
        """Track when meeting is actually booked."""
        try:
            for metric in self.email_metrics:
                if metric.email_id == email_id:
                    metric.meeting_booked_at = datetime.now()
                    metric.conversion_score = 100  # Meeting booked = 100 points (full conversion)
                    logger.success(f"🎉 MEETING BOOKED from email {email_id} by {metric.prospect_name}!")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error tracking meeting for {email_id}: {str(e)}")
            return False
    
    def get_conversion_analytics(self, days_back: int = 7) -> Dict:
        """Get powerful conversion analytics."""
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_emails = [m for m in self.email_metrics if m.sent_at >= cutoff_date]
        
        if not recent_emails:
            return {"message": "No emails sent in the specified period"}
        
        total_sent = len(recent_emails)
        total_opened = len([m for m in recent_emails if m.opened_at])
        total_clicked = len([m for m in recent_emails if m.clicked_at])
        total_meetings = len([m for m in recent_emails if m.meeting_booked_at])
        
        # Calculate conversion rates
        open_rate = (total_opened / total_sent) * 100 if total_sent > 0 else 0
        click_rate = (total_clicked / total_sent) * 100 if total_sent > 0 else 0
        meeting_rate = (total_meetings / total_sent) * 100 if total_sent > 0 else 0
        
        # Top performers
        top_subjects = {}
        for metric in recent_emails:
            subject = metric.subject
            if subject not in top_subjects:
                top_subjects[subject] = {"sent": 0, "meetings": 0}
            top_subjects[subject]["sent"] += 1
            if metric.meeting_booked_at:
                top_subjects[subject]["meetings"] += 1
        
        # Calculate conversion rate per subject
        for subject_data in top_subjects.values():
            subject_data["conversion_rate"] = (
                subject_data["meetings"] / subject_data["sent"] * 100 
                if subject_data["sent"] > 0 else 0
            )
        
        return {
            "period_days": days_back,
            "total_emails_sent": total_sent,
            "performance": {
                "open_rate": round(open_rate, 2),
                "click_rate": round(click_rate, 2),
                "meeting_conversion_rate": round(meeting_rate, 2),
                "average_conversion_score": round(
                    sum(m.conversion_score for m in recent_emails) / total_sent, 2
                ) if total_sent > 0 else 0
            },
            "meetings_booked": total_meetings,
            "top_performing_subjects": sorted(
                [{"subject": k, **v} for k, v in top_subjects.items()],
                key=lambda x: x["conversion_rate"],
                reverse=True
            )[:5],
            "recent_conversions": [
                {
                    "prospect_name": m.prospect_name,
                    "company": m.company_name,
                    "subject": m.subject,
                    "sent_at": m.sent_at.isoformat(),
                    "meeting_booked_at": m.meeting_booked_at.isoformat() if m.meeting_booked_at else None,
                    "conversion_score": m.conversion_score
                }
                for m in recent_emails if m.meeting_booked_at
            ]
        }
    
    def get_email_performance(self, email_id: str) -> Dict:
        """Get detailed performance for specific email."""
        
        for metric in self.email_metrics:
            if metric.email_id == email_id:
                return {
                    "email_id": email_id,
                    "prospect": {
                        "name": metric.prospect_name,
                        "email": metric.prospect_email,
                        "company": metric.company_name
                    },
                    "email": {
                        "subject": metric.subject,
                        "sent_at": metric.sent_at.isoformat()
                    },
                    "engagement": {
                        "opened": metric.opened_at.isoformat() if metric.opened_at else None,
                        "clicked": metric.clicked_at.isoformat() if metric.clicked_at else None,
                        "meeting_booked": metric.meeting_booked_at.isoformat() if metric.meeting_booked_at else None
                    },
                    "conversion_score": metric.conversion_score,
                    "time_to_conversion": (
                        str(metric.meeting_booked_at - metric.sent_at)
                        if metric.meeting_booked_at else None
                    )
                }
        
        return {"error": "Email not found"}

# Example usage and testing
if __name__ == "__main__":
    # Initialize sender (add your Postmark API key)
    sender = PowerfulPostmarkSender(
        postmark_api_key="your-postmark-api-key",
        from_email="your@company.com"
    )
    
    # Test email sending
    result = sender.send_powerful_email(
        prospect_email="samuel@singular.net",
        prospect_name="Samuel Hegge",
        company_name="Singular",
        subject="Boost Singular's Outbound Efficiency by 40%",
        html_body="<p>Hi Samuel,</p><p>I've been following Singular's impressive growth...</p>",
        text_body="Hi Samuel,\n\nI've been following Singular's impressive growth...",
        meeting_link="https://calendly.com/demo",
        sender_name="Sarah Johnson"
    )
    
    print("Send Result:", json.dumps(result, indent=2))
    
    # Simulate tracking events (in production, these come from webhooks)
    if result["success"]:
        email_id = result["email_id"]
        sender.track_email_opened(email_id)
        sender.track_link_clicked(email_id, "meeting")
        sender.track_meeting_booked(email_id)
    
    # Get analytics
    analytics = sender.get_conversion_analytics()
    print("\nAnalytics:", json.dumps(analytics, indent=2))