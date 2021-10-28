#include <linux/module.h>
#include <linux/vmalloc.h>
#include <net/tcp.h>


void tcp_vreno_in_ack_event(struct sock *sk, u32 flags)
{
	const struct tcp_sock *tp = tcp_sk(sk);
	const struct inet_sock *isock = inet_sk(sk);

	uint16_t sport = ntohs(isock->inet_sport);
	uint16_t dport = ntohs(isock->inet_dport);

	struct sk_buff *skb = tcp_write_queue_tail(sk);
	uint16_t length = skb == NULL ? 0 : skb->len;

	trace_printk(KERN_INFO "ACK Received. %pI4:%u %pI4:%u %d %#x %#x %u %u %u %u %u\n",
			&isock->inet_saddr, sport, &isock->inet_daddr, dport, length, tp->snd_nxt, tp->snd_una, tp->snd_cwnd, tcp_current_ssthresh(sk), tp->snd_wnd, tp->rcv_wnd, tp->srtt_us >> 3);
}


struct tcp_congestion_ops tcp_reno_verbose = {
	.flags		= TCP_CONG_NON_RESTRICTED,
	.name		= "reno_verbose",
	.owner		= THIS_MODULE,
	.ssthresh	= tcp_reno_ssthresh,
	.cong_avoid	= tcp_reno_cong_avoid,
	.undo_cwnd	= tcp_reno_undo_cwnd,
	.in_ack_event = tcp_vreno_in_ack_event,
};


static int __init tcp_reno_verbose_register(void)
{
    printk(KERN_INFO "Verbose Reno Going Up...");
	return tcp_register_congestion_control(&tcp_reno_verbose);
}


static void __exit tcp_reno_verbose_unregister(void)
{
    printk(KERN_INFO "Verbose Reno Shutting Down...");
    tcp_unregister_congestion_control(&tcp_reno_verbose);
}



module_init(tcp_reno_verbose_register);
module_exit(tcp_reno_verbose_unregister);

MODULE_AUTHOR("Yanev");
MODULE_AUTHOR("James Raphael Tiovalen");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Verbose TCP Reno");
