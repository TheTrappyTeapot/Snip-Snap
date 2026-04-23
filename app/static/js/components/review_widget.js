/* Script for app/static/js/components/review_widget.js. */

export class ReviewWidget {
    constructor(containerId, barberName = null, targetBarberId = null, targetBarbershopId = null) {
        this.container = document.getElementById(containerId);
        this.barberName = barberName;
        this.targetBarberId = targetBarberId;
        this.targetBarbershopId = targetBarbershopId;
        this.reviews = [];
        this.selectedRating = 0;
        this.renderBase();
        this.init();
    }

    async init() {
        try {
            console.log("[ReviewWidget] Initializing with targetBarberId:", this.targetBarberId, "targetBarbershopId:", this.targetBarbershopId);
            await this.fetchReviews();
            console.log("[ReviewWidget] After fetchReviews, reviews count:", this.reviews.length);
            this.renderReviews();
        } catch (e) {
            console.error("[ReviewWidget] Failed to fetch reviews:", e);
            this.renderReviews();
        }
    }

    async fetchReviews() {
        console.log("[ReviewWidget.fetchReviews] Starting, targetBarberId:", this.targetBarberId, "targetBarbershopId:", this.targetBarbershopId);
        if (!this.targetBarberId && !this.targetBarbershopId) {
            console.warn("[ReviewWidget.fetchReviews] No targetBarberId or targetBarbershopId provided, cannot fetch reviews");
            return;
        }

        try {
            let url = "/api/reviews?";
            if (this.targetBarberId) {
                url += `target_barber_id=${this.targetBarberId}`;
            } else if (this.targetBarbershopId) {
                url += `target_barbershop_id=${this.targetBarbershopId}`;
            }
            console.log("[ReviewWidget.fetchReviews] Fetching from URL:", url);
            const res = await fetch(url);
            console.log("[ReviewWidget.fetchReviews] Response status:", res.status, res.ok);
            
            if (!res.ok) {
                const err = await res.json();
                console.error("[ReviewWidget.fetchReviews] Error response:", err);
                throw new Error(err.error || "Failed to fetch reviews");
            }

            const data = await res.json();
            console.log("[ReviewWidget.fetchReviews] Success! Data received:", data);
            console.log("[ReviewWidget.fetchReviews] Review count from API:", data.reviews?.length || 0);
            
            this.reviews = (data.reviews || []).map(review => {
                const mapped = {
                    review_id: review.review_id,
                    name: "@" + review.username,
                    rating: review.rating || 0,
                    text: review.text,
                    target_barber_id: review.target_barber_id,
                    target_barbershop_id: review.target_barbershop_id,
                    target_barber_user_id: review.target_barber_user_id,
                    helpful_vote_count: review.helpful_vote_count || 0,
                    user_has_voted: review.user_has_voted || false,
                    replies: (review.replies || [])
                        // Sort replies: barber replies first (where user_id === target_barber_user_id), then by creation date
                        .sort((a, b) => {
                            const aIsBarber = a.user_id === review.target_barber_user_id ? 0 : 1;
                            const bIsBarber = b.user_id === review.target_barber_user_id ? 0 : 1;
                            if (aIsBarber !== bIsBarber) {
                                return aIsBarber - bIsBarber; // Barber replies (0) come first
                            }
                            return new Date(a.created_at) - new Date(b.created_at);
                        })
                        .map(reply => ({
                            review_id: reply.review_id,
                            user_id: reply.user_id,
                            name: "@" + reply.username,
                            text: reply.text,
                            helpful_vote_count: reply.helpful_vote_count || 0,
                            user_has_voted: reply.user_has_voted || false
                        }))
                };
                console.log("[ReviewWidget.fetchReviews] Mapped review:", mapped);
                return mapped;
            });
            
            console.log("[ReviewWidget.fetchReviews] Total reviews loaded:", this.reviews.length);
        } catch (e) {
            console.error("[ReviewWidget.fetchReviews] Exception:", e.message);
            this.reviews = [];
        }
    }

    renderBase() {
        this.container.innerHTML = `
            <div class="widget-container">
                <div class="widget-header">
                    <span>Reviews</span>
                    <div class="add-review-btn" id="openModal">＋</div>
                </div>
                <div class="review-list" id="reviewList"></div>
            </div>
            <div class="modal-overlay" id="modal">
                <div class="modal-content">
                    <div class="modal-title">Upload a review</div>
                    <div class="star-input" id="starInput">
                        <span data-v="1">★</span><span data-v="2">★</span><span data-v="3">★</span><span data-v="4">★</span><span data-v="5">★</span>
                    </div>
                    <textarea id="reviewText" placeholder="Describe your experience..."></textarea>
                    <div class="modal-btns">
                        <button class="btn-upload" id="submitReview">Upload</button>
                        <button class="btn-cancel" id="closeModal">Cancel</button>
                    </div>
                </div>
            </div>
        `;
        this.setupEventListeners();
    }

    setupEventListeners() {
        const modal = this.container.querySelector("#modal");
        this.container.querySelector("#openModal").onclick = () => modal.style.display = "flex";
        this.container.querySelector("#closeModal").onclick = () => {
            modal.style.display = "none";
            this.resetModal();
        };

        const stars = this.container.querySelectorAll("#starInput span");
        stars.forEach(s => {
            s.onclick = () => {
                this.selectedRating = parseInt(s.dataset.v);
                stars.forEach(st => st.classList.toggle("active", st.dataset.v <= this.selectedRating));
            };
        });

        this.container.querySelector("#submitReview").onclick = () => {
            const text = this.container.querySelector("#reviewText").value;
            if(!text || this.selectedRating === 0) return alert("Please add rating and text");
            
            // Save to database
            this.saveReview(text, this.selectedRating);
        };
    }

    resetModal() {
        this.selectedRating = 0;
        this.container.querySelector("#reviewText").value = "";
        this.container.querySelectorAll("#starInput span").forEach(s => s.classList.remove("active"));
    }

    renderReviews() {
        console.log("[ReviewWidget.renderReviews] Starting render with", this.reviews.length, "reviews");
        const list = this.container.querySelector("#reviewList");
        const html = this.reviews.map((rev, i) => {
            console.log(`[ReviewWidget.renderReviews] Rendering review ${i}:`, rev);
            const voteCount = rev.helpful_vote_count || 0;
            const userHasVoted = rev.user_has_voted || false;
            const voteButtonClass = userHasVoted ? 'vote-button-voted' : 'vote-button';
            const voteButtonDisabled = userHasVoted ? 'disabled' : '';
            
            return `
            <div class="review-card">
                <div class="review-name">${rev.name}</div>
                <div class="review-stars">${"★".repeat(rev.rating)}${"☆".repeat(5-rev.rating)}</div>
                <div class="review-text">${rev.text}</div>
                <div class="faded-actions">
                    <span onclick="document.getElementById('replyArea${i}').style.display='flex'">Reply</span>
                    <button class="${voteButtonClass}" ${voteButtonDisabled} onclick="window.widget.voteReview(${rev.review_id}, ${i})" title="${userHasVoted ? 'You found this helpful' : 'Mark as helpful'}">
                        👍 <span class="vote-count">${voteCount}</span>
                    </button>
                </div>
                <div class="input-box" id="replyArea${i}" style="display:none">
                    <textarea id="replyInput${i}" placeholder="Write a reply..."></textarea>
                    <div style="display: flex; gap: 8px;">
                        <button class="btn-save" onclick="window.widget.addReply(${i})">Post Reply</button>
                        <button class="btn-cancel" onclick="window.widget.cancelReply(${i})">Cancel</button>
                    </div>
                </div>
                <div class="replies-list">
                    ${rev.replies.map((rep, ri) => {
                        const isBarberReply = rep.user_id === rev.target_barber_user_id;
                        const replyVoteCount = rep.helpful_vote_count || 0;
                        const replyUserHasVoted = rep.user_has_voted || false;
                        const replyVoteButtonClass = replyUserHasVoted ? 'vote-button-voted' : 'vote-button';
                        const replyVoteButtonDisabled = replyUserHasVoted ? 'disabled' : '';
                        console.log(`[ReviewWidget.renderReviews] Review ${rev.review_id}, reply ${ri}: user_id=${rep.user_id}, target_barber_user_id=${rev.target_barber_user_id}, isBarberReply=${isBarberReply}`);
                        return `
                        <div class="reply-item" ${isBarberReply ? 'style="background-color: #f0f8ff; padding: 8px; border-left: 3px solid #007bff;"' : ''}>
                            <div style="font-weight: 500; color: #333;">${rep.name}${isBarberReply ? ' <span style="color: #007bff; font-size: 12px;">(Barber)</span>' : ''}</div>
                            <div>${rep.text}</div>
                            <div style="margin-top: 8px;">
                                <button class="${replyVoteButtonClass}" ${replyVoteButtonDisabled} onclick="window.widget.voteReview(${rep.review_id}, ${i})" title="${replyUserHasVoted ? 'You found this helpful' : 'Mark as helpful'}" style="font-size: 12px;">
                                    👍 <span class="vote-count">${replyVoteCount}</span>
                                </button>
                            </div>
                        </div>
                    `;
                    }).join("")}
                </div>
            </div>
        `}).join("");
        list.innerHTML = html;
        console.log("[ReviewWidget.renderReviews] Render complete");
    }

    addReply(i) {
        const txt = document.getElementById(`replyInput${i}`).value;
        if(!txt) return;
        
        // Save to database
        this.saveReply(i, txt);
    }

    async saveReview(text, rating) {
        try {
            const res = await fetch("/api/reviews", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    target_barber_id: this.targetBarberId || null,
                    target_barbershop_id: this.targetBarbershopId || null,
                    text: text,
                    rating: rating
                })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.error || "Failed to save review");
            }

            const data = await res.json();
            
            // Add to local state
            this.reviews.unshift({
                review_id: data.review_id,
                name: "@You",
                rating: rating,
                text: text,
                target_barber_id: this.targetBarberId || null,
                target_barbershop_id: this.targetBarbershopId || null,
                target_barber_user_id: data.target_barber_user_id || null,
                helpful_vote_count: 0,
                user_has_voted: false,
                replies: []
            });

            // Close modal and reset
            const modal = this.container.querySelector("#modal");
            modal.style.display = "none";
            this.resetModal();
            this.renderReviews();
        } catch (e) {
            alert("Error saving review: " + e.message);
        }
    }

    async saveReply(reviewIndex, text) {
        try {
            const review = this.reviews[reviewIndex];
            const res = await fetch("/api/reviews/reply", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    parent_review_id: review.review_id,
                    text: text
                })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.error || "Failed to save reply");
            }

            const data = await res.json();
            
            // Add to local state with user_id for proper highlighting
            const newReply = {
                review_id: data.reply_id,
                user_id: data.user_id,
                name: "@You",
                text: text,
                helpful_vote_count: 0,
                user_has_voted: false
            };
            
            this.reviews[reviewIndex].replies.push(newReply);
            
            // Re-sort replies so barber replies stay on top
            this.reviews[reviewIndex].replies.sort((a, b) => {
                const aIsBarber = a.user_id === review.target_barber_user_id ? 0 : 1;
                const bIsBarber = b.user_id === review.target_barber_user_id ? 0 : 1;
                return aIsBarber - bIsBarber;
            });

            // Clear and hide reply box
            document.getElementById(`replyInput${reviewIndex}`).value = "";
            document.getElementById(`replyArea${reviewIndex}`).style.display = "none";
            
            this.renderReviews();
        } catch (e) {
            alert("Error saving reply: " + e.message);
        }
    }

    async voteReview(reviewId, reviewIndex) {
        console.log(`[ReviewWidget.voteReview] Voting on review ${reviewId}`);
        
        try {
            const res = await fetch(`/api/reviews/${reviewId}/vote`, {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            });

            if (!res.ok) {
                // Try to parse as JSON, but handle HTML error pages
                let errorMsg = "Failed to vote";
                try {
                    const err = await res.json();
                    errorMsg = err.error || errorMsg;
                } catch (parseErr) {
                    // Response wasn't JSON (probably HTML error page)
                    console.log(`[ReviewWidget.voteReview] Non-JSON response (${res.status}):`, res);
                    errorMsg = `Server error: ${res.status} ${res.statusText}`;
                }
                
                if (res.status === 401) {
                    alert("Please log in to vote");
                    return;
                }
                throw new Error(errorMsg);
            }

            const data = await res.json();
            
            // Find and update the review/reply in our local state
            // Check if it's a parent review or a reply
            let found = false;
            
            for (let i = 0; i < this.reviews.length; i++) {
                if (this.reviews[i].review_id === reviewId) {
                    this.reviews[i].helpful_vote_count = data.helpful_vote_count;
                    this.reviews[i].user_has_voted = true;
                    found = true;
                    console.log(`[ReviewWidget.voteReview] Updated parent review ${reviewId}`);
                    break;
                }
                
                // Check replies
                for (let j = 0; j < this.reviews[i].replies.length; j++) {
                    if (this.reviews[i].replies[j].review_id === reviewId) {
                        this.reviews[i].replies[j].helpful_vote_count = data.helpful_vote_count;
                        this.reviews[i].replies[j].user_has_voted = true;
                        found = true;
                        console.log(`[ReviewWidget.voteReview] Updated reply ${reviewId}`);
                        break;
                    }
                }
                if (found) break;
            }
            
            this.renderReviews();
        } catch (e) {
            alert("Error voting: " + e.message);
        }
    }

    cancelReply(i) {
        document.getElementById(`replyInput${i}`).value = "";
        document.getElementById(`replyArea${i}`).style.display = "none";
    }
}
